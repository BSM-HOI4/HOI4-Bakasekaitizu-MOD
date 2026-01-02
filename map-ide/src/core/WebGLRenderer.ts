/**
 * High-Performance Map Renderer
 * Uses WebGL2 for GPU-accelerated rendering with Canvas 2D fallback
 * Features: Smooth rendering, GPU texture caching, efficient updates
 */

import { RGB, Province, State, StrategicRegion, AIArea } from '../types';

export interface BorderSegment {
  points: Float32Array;
  color: [number, number, number, number];
}

export interface RenderState {
  zoom: number;
  panX: number;
  panY: number;
  viewportWidth: number;
  viewportHeight: number;
  showGrid: boolean;
  showBorders: boolean;
  selectedProvinceId: number | null;
  hoveredProvinceId: number | null;
  activeLayer: 'provinces' | 'states' | 'strategicRegions' | 'aiAreas';
  layerOpacity: number;
}

// Vertex shader for WebGL rendering
const VERTEX_SHADER_SOURCE = `#version 300 es
precision highp float;

in vec2 a_position;
in vec2 a_texCoord;

uniform vec2 u_resolution;
uniform vec2 u_translation;
uniform float u_scale;

out vec2 v_texCoord;

void main() {
  // Apply pan and zoom
  vec2 scaled = a_position * u_scale;
  vec2 translated = scaled + u_translation;
  
  // Convert to clip space (-1 to 1)
  vec2 clipSpace = (translated / u_resolution) * 2.0 - 1.0;
  
  gl_Position = vec4(clipSpace * vec2(1, -1), 0, 1);
  v_texCoord = a_texCoord;
}
`;

// Fragment shader for map rendering with smooth zoom
const FRAGMENT_SHADER_SOURCE = `#version 300 es
precision highp float;

in vec2 v_texCoord;

uniform sampler2D u_mapTexture;
uniform sampler2D u_highlightTexture;
uniform float u_zoom;
uniform bool u_useSmoothing;

out vec4 outColor;

void main() {
  // Get base map color
  vec4 mapColor;
  
  if (u_useSmoothing && u_zoom < 4.0) {
    // Use bilinear filtering for smoother rendering at low zoom
    mapColor = texture(u_mapTexture, v_texCoord);
  } else {
    // Use nearest neighbor for pixel-perfect at high zoom
    mapColor = texture(u_mapTexture, v_texCoord);
  }
  
  // Get highlight overlay
  vec4 highlight = texture(u_highlightTexture, v_texCoord);
  
  // Blend highlight over map
  outColor = mix(mapColor, highlight, highlight.a);
}
`;

// Vertex shader for border/grid lines
const LINE_VERTEX_SHADER = `#version 300 es
precision highp float;

in vec2 a_position;

uniform vec2 u_resolution;
uniform vec2 u_translation;
uniform float u_scale;

void main() {
  vec2 scaled = a_position * u_scale;
  vec2 translated = scaled + u_translation;
  vec2 clipSpace = (translated / u_resolution) * 2.0 - 1.0;
  gl_Position = vec4(clipSpace * vec2(1, -1), 0, 1);
  gl_PointSize = 2.0;
}
`;

// Fragment shader for lines
const LINE_FRAGMENT_SHADER = `#version 300 es
precision highp float;

uniform vec4 u_color;
out vec4 outColor;

void main() {
  outColor = u_color;
}
`;

/**
 * WebGL2 Renderer with Canvas 2D fallback
 */
export class WebGLRenderer {
  private canvas: HTMLCanvasElement;
  private gl: WebGL2RenderingContext | null = null;
  private ctx: CanvasRenderingContext2D | null = null;
  private useWebGL: boolean = false;
  
  // Map data
  private mapWidth: number = 0;
  private mapHeight: number = 0;
  private provincePixelData: Uint8Array | null = null;
  
  // WebGL resources
  private mapProgram: WebGLProgram | null = null;
  private lineProgram: WebGLProgram | null = null;
  private mapTexture: WebGLTexture | null = null;
  private highlightTexture: WebGLTexture | null = null;
  private quadVAO: WebGLVertexArrayObject | null = null;
  private quadBuffer: WebGLBuffer | null = null;
  private texCoordBuffer: WebGLBuffer | null = null;
  private lineVAO: WebGLVertexArrayObject | null = null;
  private lineBuffer: WebGLBuffer | null = null;
  
  // Canvas 2D fallback resources
  private mapImageData: ImageData | null = null;
  private highlightImageData: ImageData | null = null;
  private offscreenCanvas: OffscreenCanvas | null = null;
  private offscreenCtx: OffscreenCanvasRenderingContext2D | null = null;
  
  // Cached border data
  private stateBorders: Map<number, BorderSegment> = new Map();
  private strategicRegionBorders: Map<number, BorderSegment> = new Map();
  private aiAreaBorders: Map<string, BorderSegment> = new Map();
  
  // Selection state
  private selectedProvince: Province | null = null;
  private hoveredProvince: Province | null = null;
  private highlightDirty: boolean = true;

  constructor(canvas: HTMLCanvasElement) {
    this.canvas = canvas;
    
    // Try WebGL2 first
    const gl = canvas.getContext('webgl2', {
      alpha: false,
      antialias: true,
      powerPreference: 'high-performance',
      preserveDrawingBuffer: false,
    }) as WebGL2RenderingContext | null;
    
    if (gl) {
      this.gl = gl;
      this.useWebGL = true;
      this.initWebGL();
      console.log('WebGL2 renderer initialized');
    } else {
      // Fallback to Canvas 2D
      const ctx = canvas.getContext('2d', {
        alpha: false,
        desynchronized: true,
      });
      
      if (!ctx) {
        throw new Error('Neither WebGL2 nor Canvas 2D context is available');
      }
      
      this.ctx = ctx;
      this.useWebGL = false;
      console.log('Canvas 2D fallback renderer initialized');
    }
  }

  /**
   * Initialize WebGL2 resources
   */
  private initWebGL(): void {
    const gl = this.gl!;
    
    // Create shaders and programs
    this.mapProgram = this.createProgram(VERTEX_SHADER_SOURCE, FRAGMENT_SHADER_SOURCE);
    this.lineProgram = this.createProgram(LINE_VERTEX_SHADER, LINE_FRAGMENT_SHADER);
    
    if (!this.mapProgram || !this.lineProgram) {
      console.warn('Failed to create shaders, falling back to Canvas 2D');
      this.useWebGL = false;
      this.ctx = this.canvas.getContext('2d');
      return;
    }
    
    // Create quad geometry for map rendering
    this.createQuadVAO();
    
    // Create line VAO
    this.createLineVAO();
    
    // Create textures
    this.mapTexture = this.createTexture();
    this.highlightTexture = this.createTexture();
    
    // Enable blending
    gl.enable(gl.BLEND);
    gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
  }

  private createProgram(vertexSource: string, fragmentSource: string): WebGLProgram | null {
    const gl = this.gl!;
    
    const vertexShader = gl.createShader(gl.VERTEX_SHADER);
    const fragmentShader = gl.createShader(gl.FRAGMENT_SHADER);
    
    if (!vertexShader || !fragmentShader) return null;
    
    gl.shaderSource(vertexShader, vertexSource);
    gl.compileShader(vertexShader);
    
    if (!gl.getShaderParameter(vertexShader, gl.COMPILE_STATUS)) {
      console.error('Vertex shader error:', gl.getShaderInfoLog(vertexShader));
      return null;
    }
    
    gl.shaderSource(fragmentShader, fragmentSource);
    gl.compileShader(fragmentShader);
    
    if (!gl.getShaderParameter(fragmentShader, gl.COMPILE_STATUS)) {
      console.error('Fragment shader error:', gl.getShaderInfoLog(fragmentShader));
      return null;
    }
    
    const program = gl.createProgram();
    if (!program) return null;
    
    gl.attachShader(program, vertexShader);
    gl.attachShader(program, fragmentShader);
    gl.linkProgram(program);
    
    if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
      console.error('Program link error:', gl.getProgramInfoLog(program));
      return null;
    }
    
    // Clean up shaders
    gl.deleteShader(vertexShader);
    gl.deleteShader(fragmentShader);
    
    return program;
  }

  private createQuadVAO(): void {
    const gl = this.gl!;
    
    // Create VAO
    this.quadVAO = gl.createVertexArray();
    gl.bindVertexArray(this.quadVAO);
    
    // Create position buffer - will be updated when map is loaded
    this.quadBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, this.quadBuffer);
    
    // Get attribute location
    const posLoc = gl.getAttribLocation(this.mapProgram!, 'a_position');
    gl.enableVertexAttribArray(posLoc);
    gl.vertexAttribPointer(posLoc, 2, gl.FLOAT, false, 0, 0);
    
    // Create texCoord buffer
    this.texCoordBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, this.texCoordBuffer);
    
    // Texture coordinates (standard UV mapping)
    const texCoords = new Float32Array([
      0, 0,  // top-left
      1, 0,  // top-right
      0, 1,  // bottom-left
      0, 1,  // bottom-left
      1, 0,  // top-right
      1, 1,  // bottom-right
    ]);
    gl.bufferData(gl.ARRAY_BUFFER, texCoords, gl.STATIC_DRAW);
    
    const texLoc = gl.getAttribLocation(this.mapProgram!, 'a_texCoord');
    gl.enableVertexAttribArray(texLoc);
    gl.vertexAttribPointer(texLoc, 2, gl.FLOAT, false, 0, 0);
    
    gl.bindVertexArray(null);
  }

  private createLineVAO(): void {
    const gl = this.gl!;
    
    this.lineVAO = gl.createVertexArray();
    gl.bindVertexArray(this.lineVAO);
    
    this.lineBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, this.lineBuffer);
    
    const posLoc = gl.getAttribLocation(this.lineProgram!, 'a_position');
    gl.enableVertexAttribArray(posLoc);
    gl.vertexAttribPointer(posLoc, 2, gl.FLOAT, false, 0, 0);
    
    gl.bindVertexArray(null);
  }

  private createTexture(): WebGLTexture | null {
    const gl = this.gl!;
    
    const texture = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, texture);
    
    // Set texture parameters - NEAREST for pixel-perfect at high zoom
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.NEAREST);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST);
    
    return texture;
  }

  /**
   * Upload map pixel data
   */
  uploadMapData(pixels: Uint8Array, width: number, height: number): void {
    console.log('[WebGLRenderer] uploadMapData called:', width, 'x', height, 'pixels:', pixels.length);
    this.mapWidth = width;
    this.mapHeight = height;
    this.provincePixelData = new Uint8Array(pixels);
    
    if (this.useWebGL && this.gl) {
      console.log('[WebGLRenderer] Using WebGL path');
      this.uploadMapTextureWebGL(pixels, width, height);
      this.updateQuadBuffer();
    } else {
      console.log('[WebGLRenderer] Using Canvas 2D path');
      this.createMapImageData(pixels, width, height);
    }
    
    // Create offscreen canvas for highlight overlay
    this.offscreenCanvas = new OffscreenCanvas(width, height);
    this.offscreenCtx = this.offscreenCanvas.getContext('2d');
    
    this.highlightDirty = true;
    console.log('[WebGLRenderer] uploadMapData complete. mapWidth:', this.mapWidth, 'mapHeight:', this.mapHeight);
  }

  private uploadMapTextureWebGL(pixels: Uint8Array, width: number, height: number): void {
    console.log('[WebGLRenderer] uploadMapTextureWebGL called');
    const gl = this.gl!;
    
    // Convert RGB to RGBA for WebGL
    const rgbaData = new Uint8Array(width * height * 4);
    for (let i = 0; i < width * height; i++) {
      rgbaData[i * 4] = pixels[i * 3];       // R
      rgbaData[i * 4 + 1] = pixels[i * 3 + 1]; // G
      rgbaData[i * 4 + 2] = pixels[i * 3 + 2]; // B
      rgbaData[i * 4 + 3] = 255;             // A
    }
    
    gl.bindTexture(gl.TEXTURE_2D, this.mapTexture);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, width, height, 0, gl.RGBA, gl.UNSIGNED_BYTE, rgbaData);
  }

  private updateQuadBuffer(): void {
    const gl = this.gl!;
    
    // Create quad covering the map dimensions
    const positions = new Float32Array([
      0, 0,                           // top-left
      this.mapWidth, 0,               // top-right
      0, this.mapHeight,              // bottom-left
      0, this.mapHeight,              // bottom-left
      this.mapWidth, 0,               // top-right
      this.mapWidth, this.mapHeight,  // bottom-right
    ]);
    
    gl.bindBuffer(gl.ARRAY_BUFFER, this.quadBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, positions, gl.STATIC_DRAW);
  }

  private createMapImageData(pixels: Uint8Array, width: number, height: number): void {
    console.log('[WebGLRenderer] createMapImageData called');
    this.mapImageData = new ImageData(width, height);
    const data = this.mapImageData.data;
    
    for (let i = 0; i < width * height; i++) {
      data[i * 4] = pixels[i * 3];       // R
      data[i * 4 + 1] = pixels[i * 3 + 1]; // G
      data[i * 4 + 2] = pixels[i * 3 + 2]; // B
      data[i * 4 + 3] = 255;             // A
    }
  }

  /**
   * Update map texture from modified pixel data
   */
  updateMapTexture(pixels: Uint8Array): void {
    if (!this.mapWidth || !this.mapHeight) return;
    
    this.provincePixelData = new Uint8Array(pixels);
    
    if (this.useWebGL && this.gl) {
      this.uploadMapTextureWebGL(pixels, this.mapWidth, this.mapHeight);
    } else {
      this.createMapImageData(pixels, this.mapWidth, this.mapHeight);
    }
  }

  /**
   * Generate border segments for states
   */
  generateStateBorders(
    states: Map<number, State>,
    _provinces: Map<number, Province>,
    provinceByColor: Map<string, Province>
  ): void {
    this.stateBorders.clear();
    
    const provinceToState = new Map<number, number>();
    for (const [stateId, state] of states) {
      for (const provinceId of state.provinces) {
        provinceToState.set(provinceId, stateId);
      }
    }
    
    if (!this.provincePixelData) return;
    
    const borderPixels = this.detectBorders(
      provinceByColor,
      (p1, p2) => provinceToState.get(p1?.id ?? -1) !== provinceToState.get(p2?.id ?? -1)
    );
    
    for (const [stateId, state] of states) {
      const stateProvinces = new Set(state.provinces);
      const points: number[] = [];
      
      for (const [x, y] of borderPixels) {
        const color = this.getPixelColor(x, y);
        const key = `${color.r},${color.g},${color.b}`;
        const province = provinceByColor.get(key);
        if (province && stateProvinces.has(province.id)) {
          points.push(x, y);
        }
      }
      
      if (points.length > 0) {
        this.stateBorders.set(stateId, {
          points: new Float32Array(points),
          color: [1.0, 0.8, 0.0, 0.8], // Orange
        });
      }
    }
  }

  /**
   * Generate border segments for strategic regions
   */
  generateStrategicRegionBorders(
    regions: Map<number, StrategicRegion>,
    _provinces: Map<number, Province>,
    provinceByColor: Map<string, Province>
  ): void {
    this.strategicRegionBorders.clear();
    
    const provinceToRegion = new Map<number, number>();
    for (const [regionId, region] of regions) {
      for (const provinceId of region.provinces) {
        provinceToRegion.set(provinceId, regionId);
      }
    }
    
    if (!this.provincePixelData) return;
    
    const borderPixels = this.detectBorders(
      provinceByColor,
      (p1, p2) => provinceToRegion.get(p1?.id ?? -1) !== provinceToRegion.get(p2?.id ?? -1)
    );
    
    for (const [regionId, region] of regions) {
      const regionProvinces = new Set(region.provinces);
      const points: number[] = [];
      
      for (const [x, y] of borderPixels) {
        const color = this.getPixelColor(x, y);
        const key = `${color.r},${color.g},${color.b}`;
        const province = provinceByColor.get(key);
        if (province && regionProvinces.has(province.id)) {
          points.push(x, y);
        }
      }
      
      if (points.length > 0) {
        this.strategicRegionBorders.set(regionId, {
          points: new Float32Array(points),
          color: [0.0, 0.8, 1.0, 0.8], // Cyan
        });
      }
    }
  }

  /**
   * Generate border segments for AI areas
   */
  generateAIAreaBorders(
    aiAreas: AIArea[],
    regions: Map<number, StrategicRegion>,
    _provinces: Map<number, Province>,
    provinceByColor: Map<string, Province>
  ): void {
    this.aiAreaBorders.clear();
    
    const provinceToArea = new Map<number, string>();
    for (const area of aiAreas) {
      if (area.strategicRegions) {
        for (const regionId of area.strategicRegions) {
          const region = regions.get(regionId);
          if (region) {
            for (const provinceId of region.provinces) {
              provinceToArea.set(provinceId, area.name);
            }
          }
        }
      }
    }
    
    if (!this.provincePixelData) return;
    
    const borderPixels = this.detectBorders(
      provinceByColor,
      (p1, p2) => provinceToArea.get(p1?.id ?? -1) !== provinceToArea.get(p2?.id ?? -1)
    );
    
    for (const area of aiAreas) {
      const areaProvinces = new Set<number>();
      if (area.strategicRegions) {
        for (const regionId of area.strategicRegions) {
          const region = regions.get(regionId);
          if (region) {
            for (const provinceId of region.provinces) {
              areaProvinces.add(provinceId);
            }
          }
        }
      }
      
      const points: number[] = [];
      for (const [x, y] of borderPixels) {
        const color = this.getPixelColor(x, y);
        const key = `${color.r},${color.g},${color.b}`;
        const province = provinceByColor.get(key);
        if (province && areaProvinces.has(province.id)) {
          points.push(x, y);
        }
      }
      
      if (points.length > 0) {
        this.aiAreaBorders.set(area.name, {
          points: new Float32Array(points),
          color: [1.0, 0.0, 0.8, 0.8], // Magenta
        });
      }
    }
  }

  private detectBorders(
    provinceByColor: Map<string, Province>,
    isBoundary: (p1: Province | undefined, p2: Province | undefined) => boolean
  ): [number, number][] {
    const borderPixels: [number, number][] = [];
    
    if (!this.provincePixelData) return borderPixels;
    
    const width = this.mapWidth;
    const height = this.mapHeight;
    const step = Math.max(1, Math.floor(width / 1024));
    
    for (let y = 0; y < height - 1; y += step) {
      for (let x = 0; x < width - 1; x += step) {
        const color1 = this.getPixelColor(x, y);
        const color2 = this.getPixelColor(x + 1, y);
        const color3 = this.getPixelColor(x, y + 1);
        
        const key1 = `${color1.r},${color1.g},${color1.b}`;
        const key2 = `${color2.r},${color2.g},${color2.b}`;
        const key3 = `${color3.r},${color3.g},${color3.b}`;
        
        const p1 = provinceByColor.get(key1);
        const p2 = provinceByColor.get(key2);
        const p3 = provinceByColor.get(key3);
        
        if (isBoundary(p1, p2) || isBoundary(p1, p3)) {
          borderPixels.push([x, y]);
        }
      }
    }
    
    return borderPixels;
  }

  private getPixelColor(x: number, y: number): RGB {
    if (!this.provincePixelData) return { r: 0, g: 0, b: 0 };
    
    const idx = (y * this.mapWidth + x) * 3;
    return {
      r: this.provincePixelData[idx],
      g: this.provincePixelData[idx + 1],
      b: this.provincePixelData[idx + 2],
    };
  }

  /**
   * Update highlight overlay for selected/hovered province
   */
  updateHighlightOverlay(
    selectedProvinceId: number | null,
    hoveredProvinceId: number | null,
    provinces: Map<number, Province>
  ): void {
    const newSelected = selectedProvinceId ? provinces.get(selectedProvinceId) || null : null;
    const newHovered = hoveredProvinceId ? provinces.get(hoveredProvinceId) || null : null;
    
    if (this.selectedProvince !== newSelected || this.hoveredProvince !== newHovered) {
      this.selectedProvince = newSelected;
      this.hoveredProvince = newHovered;
      this.highlightDirty = true;
    }
  }

  private updateHighlightTexture(): void {
    if (!this.highlightDirty || !this.provincePixelData) return;
    
    const width = this.mapWidth;
    const height = this.mapHeight;
    
    // Create highlight data
    const highlightData = new Uint8Array(width * height * 4);
    
    for (let i = 0; i < width * height; i++) {
      const r = this.provincePixelData[i * 3];
      const g = this.provincePixelData[i * 3 + 1];
      const b = this.provincePixelData[i * 3 + 2];
      
      if (this.selectedProvince &&
          r === this.selectedProvince.color.r &&
          g === this.selectedProvince.color.g &&
          b === this.selectedProvince.color.b) {
        // Yellow highlight for selected
        highlightData[i * 4] = 255;
        highlightData[i * 4 + 1] = 200;
        highlightData[i * 4 + 2] = 0;
        highlightData[i * 4 + 3] = 100;
      } else if (this.hoveredProvince &&
                 r === this.hoveredProvince.color.r &&
                 g === this.hoveredProvince.color.g &&
                 b === this.hoveredProvince.color.b) {
        // Light blue highlight for hovered
        highlightData[i * 4] = 100;
        highlightData[i * 4 + 1] = 200;
        highlightData[i * 4 + 2] = 255;
        highlightData[i * 4 + 3] = 60;
      } else {
        highlightData[i * 4 + 3] = 0; // Transparent
      }
    }
    
    if (this.useWebGL && this.gl) {
      const gl = this.gl;
      gl.bindTexture(gl.TEXTURE_2D, this.highlightTexture);
      gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, width, height, 0, gl.RGBA, gl.UNSIGNED_BYTE, highlightData);
    } else if (this.offscreenCtx) {
      this.highlightImageData = new ImageData(new Uint8ClampedArray(highlightData), width, height);
    }
    
    this.highlightDirty = false;
  }

  /**
   * Main render function
   */
  render(state: RenderState): void {
    // Resize canvas if needed
    if (this.canvas.width !== state.viewportWidth || this.canvas.height !== state.viewportHeight) {
      this.canvas.width = state.viewportWidth;
      this.canvas.height = state.viewportHeight;
      console.log('[WebGLRenderer] Canvas resized to', state.viewportWidth, 'x', state.viewportHeight);
    }
    
    // Update highlight texture if dirty
    this.updateHighlightTexture();
    
    if (this.useWebGL && this.gl) {
      this.renderWebGL(state);
    } else if (this.ctx) {
      this.renderCanvas2D(state);
    }
  }

  private renderWebGL(state: RenderState): void {
    const gl = this.gl!;
    
    // Set viewport
    gl.viewport(0, 0, state.viewportWidth, state.viewportHeight);
    
    // Clear with dark background
    gl.clearColor(0.12, 0.12, 0.12, 1.0);
    gl.clear(gl.COLOR_BUFFER_BIT);
    
    if (!this.mapWidth || !this.mapHeight || !this.mapProgram) {
      // Log only once to avoid spam
      return;
    }
    
    // Use map program
    gl.useProgram(this.mapProgram);
    
    // Set uniforms
    const resLoc = gl.getUniformLocation(this.mapProgram, 'u_resolution');
    const transLoc = gl.getUniformLocation(this.mapProgram, 'u_translation');
    const scaleLoc = gl.getUniformLocation(this.mapProgram, 'u_scale');
    const zoomLoc = gl.getUniformLocation(this.mapProgram, 'u_zoom');
    const smoothLoc = gl.getUniformLocation(this.mapProgram, 'u_useSmoothing');
    const mapTexLoc = gl.getUniformLocation(this.mapProgram, 'u_mapTexture');
    const highlightTexLoc = gl.getUniformLocation(this.mapProgram, 'u_highlightTexture');
    
    gl.uniform2f(resLoc, state.viewportWidth, state.viewportHeight);
    gl.uniform2f(transLoc, state.panX, state.panY);
    gl.uniform1f(scaleLoc, state.zoom);
    gl.uniform1f(zoomLoc, state.zoom);
    gl.uniform1i(smoothLoc, state.zoom < 4 ? 1 : 0);
    
    // Bind textures
    gl.activeTexture(gl.TEXTURE0);
    gl.bindTexture(gl.TEXTURE_2D, this.mapTexture);
    gl.uniform1i(mapTexLoc, 0);
    
    gl.activeTexture(gl.TEXTURE1);
    gl.bindTexture(gl.TEXTURE_2D, this.highlightTexture);
    gl.uniform1i(highlightTexLoc, 1);
    
    // Update texture filtering based on zoom
    gl.bindTexture(gl.TEXTURE_2D, this.mapTexture);
    if (state.zoom >= 4) {
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.NEAREST);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST);
    } else {
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
    }
    
    // Draw map
    gl.bindVertexArray(this.quadVAO);
    gl.drawArrays(gl.TRIANGLES, 0, 6);
    
    // Draw borders
    if (state.showBorders) {
      this.renderBordersWebGL(state);
    }
    
    // Draw grid at high zoom
    if (state.showGrid && state.zoom >= 8) {
      this.renderGridWebGL(state);
    }
  }

  private renderBordersWebGL(state: RenderState): void {
    const gl = this.gl!;
    
    if (!this.lineProgram) return;
    
    let borders: Map<number | string, BorderSegment>;
    
    switch (state.activeLayer) {
      case 'states':
        borders = this.stateBorders as Map<number | string, BorderSegment>;
        break;
      case 'strategicRegions':
        borders = this.strategicRegionBorders as Map<number | string, BorderSegment>;
        break;
      case 'aiAreas':
        borders = this.aiAreaBorders;
        break;
      default:
        return;
    }
    
    gl.useProgram(this.lineProgram);
    
    const resLoc = gl.getUniformLocation(this.lineProgram, 'u_resolution');
    const transLoc = gl.getUniformLocation(this.lineProgram, 'u_translation');
    const scaleLoc = gl.getUniformLocation(this.lineProgram, 'u_scale');
    const colorLoc = gl.getUniformLocation(this.lineProgram, 'u_color');
    
    gl.uniform2f(resLoc, state.viewportWidth, state.viewportHeight);
    gl.uniform2f(transLoc, state.panX, state.panY);
    gl.uniform1f(scaleLoc, state.zoom);
    
    gl.bindVertexArray(this.lineVAO);
    
    for (const [, segment] of borders) {
      gl.uniform4fv(colorLoc, segment.color);
      
      gl.bindBuffer(gl.ARRAY_BUFFER, this.lineBuffer);
      gl.bufferData(gl.ARRAY_BUFFER, segment.points, gl.DYNAMIC_DRAW);
      
      gl.drawArrays(gl.POINTS, 0, segment.points.length / 2);
    }
  }

  private renderGridWebGL(state: RenderState): void {
    const gl = this.gl!;
    
    if (!this.lineProgram) return;
    
    // Calculate visible area
    const startX = Math.max(0, Math.floor(-state.panX / state.zoom));
    const startY = Math.max(0, Math.floor(-state.panY / state.zoom));
    const endX = Math.min(this.mapWidth, Math.ceil((state.viewportWidth - state.panX) / state.zoom));
    const endY = Math.min(this.mapHeight, Math.ceil((state.viewportHeight - state.panY) / state.zoom));
    
    // Generate grid lines
    const gridPoints: number[] = [];
    
    // Vertical lines
    for (let x = startX; x <= endX; x++) {
      gridPoints.push(x, startY, x, endY);
    }
    
    // Horizontal lines
    for (let y = startY; y <= endY; y++) {
      gridPoints.push(startX, y, endX, y);
    }
    
    if (gridPoints.length === 0) return;
    
    gl.useProgram(this.lineProgram);
    
    const resLoc = gl.getUniformLocation(this.lineProgram, 'u_resolution');
    const transLoc = gl.getUniformLocation(this.lineProgram, 'u_translation');
    const scaleLoc = gl.getUniformLocation(this.lineProgram, 'u_scale');
    const colorLoc = gl.getUniformLocation(this.lineProgram, 'u_color');
    
    gl.uniform2f(resLoc, state.viewportWidth, state.viewportHeight);
    gl.uniform2f(transLoc, state.panX, state.panY);
    gl.uniform1f(scaleLoc, state.zoom);
    gl.uniform4f(colorLoc, 0.4, 0.4, 0.4, 0.3);
    
    gl.bindVertexArray(this.lineVAO);
    gl.bindBuffer(gl.ARRAY_BUFFER, this.lineBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(gridPoints), gl.DYNAMIC_DRAW);
    
    gl.drawArrays(gl.LINES, 0, gridPoints.length / 2);
  }

  private renderCanvas2D(state: RenderState): void {
    const ctx = this.ctx!;
    
    // Disable smoothing for pixel-perfect at high zoom
    ctx.imageSmoothingEnabled = state.zoom < 4;
    ctx.imageSmoothingQuality = 'high';
    
    // Clear canvas with dark background
    ctx.fillStyle = '#1e1e1e';
    ctx.fillRect(0, 0, state.viewportWidth, state.viewportHeight);
    
    if (!this.mapWidth || !this.mapHeight || !this.mapImageData) {
      // Log only once to avoid spam
      return;
    }
    
    // Save context state
    ctx.save();
    
    // Apply pan and zoom transformation
    ctx.translate(state.panX, state.panY);
    ctx.scale(state.zoom, state.zoom);
    
    // Draw map
    this.renderMapCanvas2D(ctx);
    
    // Draw selection highlights
    this.renderHighlightsCanvas2D(ctx);
    
    // Draw borders
    if (state.showBorders) {
      this.renderBordersCanvas2D(ctx, state);
    }
    
    // Draw grid at high zoom
    if (state.showGrid && state.zoom >= 8) {
      this.renderGridCanvas2D(ctx, state);
    }
    
    // Restore context state
    ctx.restore();
  }

  private renderMapCanvas2D(ctx: CanvasRenderingContext2D): void {
    if (!this.mapImageData) return;
    
    // Use offscreen canvas for better performance
    if (!this.offscreenCanvas || !this.offscreenCtx) {
      this.offscreenCanvas = new OffscreenCanvas(this.mapWidth, this.mapHeight);
      this.offscreenCtx = this.offscreenCanvas.getContext('2d');
    }
    
    if (this.offscreenCtx) {
      this.offscreenCtx.putImageData(this.mapImageData, 0, 0);
      ctx.drawImage(this.offscreenCanvas, 0, 0);
    }
  }

  private renderHighlightsCanvas2D(ctx: CanvasRenderingContext2D): void {
    if (!this.highlightImageData || !this.offscreenCtx) return;
    
    // Create temporary canvas for highlight
    const highlightCanvas = new OffscreenCanvas(this.mapWidth, this.mapHeight);
    const hCtx = highlightCanvas.getContext('2d');
    
    if (hCtx) {
      hCtx.putImageData(this.highlightImageData, 0, 0);
      ctx.globalCompositeOperation = 'source-over';
      ctx.drawImage(highlightCanvas, 0, 0);
    }
  }

  private renderBordersCanvas2D(ctx: CanvasRenderingContext2D, state: RenderState): void {
    let borders: Map<number | string, BorderSegment>;
    
    switch (state.activeLayer) {
      case 'states':
        borders = this.stateBorders as Map<number | string, BorderSegment>;
        break;
      case 'strategicRegions':
        borders = this.strategicRegionBorders as Map<number | string, BorderSegment>;
        break;
      case 'aiAreas':
        borders = this.aiAreaBorders;
        break;
      default:
        return;
    }
    
    const pointSize = Math.max(1, 2 / state.zoom);
    
    for (const [, segment] of borders) {
      const [r, g, b, a] = segment.color;
      ctx.fillStyle = `rgba(${Math.round(r * 255)}, ${Math.round(g * 255)}, ${Math.round(b * 255)}, ${a})`;
      
      const points = segment.points;
      for (let i = 0; i < points.length; i += 2) {
        ctx.fillRect(points[i], points[i + 1], pointSize, pointSize);
      }
    }
  }

  private renderGridCanvas2D(ctx: CanvasRenderingContext2D, state: RenderState): void {
    const startX = Math.max(0, Math.floor(-state.panX / state.zoom));
    const startY = Math.max(0, Math.floor(-state.panY / state.zoom));
    const endX = Math.min(this.mapWidth, Math.ceil((state.viewportWidth - state.panX) / state.zoom));
    const endY = Math.min(this.mapHeight, Math.ceil((state.viewportHeight - state.panY) / state.zoom));
    
    ctx.strokeStyle = 'rgba(100, 100, 100, 0.3)';
    ctx.lineWidth = 1 / state.zoom;
    
    ctx.beginPath();
    
    // Vertical lines
    for (let x = startX; x <= endX; x++) {
      ctx.moveTo(x, startY);
      ctx.lineTo(x, endY);
    }
    
    // Horizontal lines
    for (let y = startY; y <= endY; y++) {
      ctx.moveTo(startX, y);
      ctx.lineTo(endX, y);
    }
    
    ctx.stroke();
  }

  /**
   * Resize the renderer viewport
   */
  resize(width: number, height: number): void {
    this.canvas.width = width;
    this.canvas.height = height;
  }

  /**
   * Get map dimensions
   */
  getMapDimensions(): { width: number; height: number } {
    return { width: this.mapWidth, height: this.mapHeight };
  }

  /**
   * Get renderer type
   */
  getRendererType(): 'webgl' | 'canvas2d' {
    return this.useWebGL ? 'webgl' : 'canvas2d';
  }

  /**
   * Cleanup resources
   */
  dispose(): void {
    if (this.gl) {
      const gl = this.gl;
      
      if (this.mapTexture) gl.deleteTexture(this.mapTexture);
      if (this.highlightTexture) gl.deleteTexture(this.highlightTexture);
      if (this.quadVAO) gl.deleteVertexArray(this.quadVAO);
      if (this.lineVAO) gl.deleteVertexArray(this.lineVAO);
      if (this.quadBuffer) gl.deleteBuffer(this.quadBuffer);
      if (this.texCoordBuffer) gl.deleteBuffer(this.texCoordBuffer);
      if (this.lineBuffer) gl.deleteBuffer(this.lineBuffer);
      if (this.mapProgram) gl.deleteProgram(this.mapProgram);
      if (this.lineProgram) gl.deleteProgram(this.lineProgram);
    }
    
    this.mapImageData = null;
    this.highlightImageData = null;
    this.provincePixelData = null;
    this.offscreenCanvas = null;
    this.offscreenCtx = null;
  }
}
