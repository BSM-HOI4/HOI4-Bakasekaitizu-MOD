/**
 * WebGL2 Renderer for high-performance map rendering
 * Supports multiple overlay layers (provinces, states, strategic regions, AI areas)
 */

import { RGB, Province, State, StrategicRegion, AIArea } from '../types';

// Shader source code
const VERTEX_SHADER_SOURCE = `#version 300 es
precision highp float;

in vec2 a_position;
in vec2 a_texCoord;

out vec2 v_texCoord;

uniform vec2 u_resolution;
uniform vec2 u_translation;
uniform float u_scale;

void main() {
    vec2 position = (a_position * u_scale + u_translation) / u_resolution * 2.0 - 1.0;
    position.y = -position.y; // Flip Y for WebGL coordinate system
    gl_Position = vec4(position, 0, 1);
    v_texCoord = a_texCoord;
}
`;

const FRAGMENT_SHADER_SOURCE = `#version 300 es
precision highp float;

in vec2 v_texCoord;
out vec4 outColor;

uniform sampler2D u_mapTexture;
uniform sampler2D u_overlayTexture;
uniform float u_overlayOpacity;
uniform bool u_hasOverlay;
uniform vec4 u_highlightColor;
uniform bool u_hasHighlight;

void main() {
    vec4 mapColor = texture(u_mapTexture, v_texCoord);
    
    if (u_hasOverlay) {
        vec4 overlayColor = texture(u_overlayTexture, v_texCoord);
        if (overlayColor.a > 0.0) {
            mapColor = mix(mapColor, overlayColor, overlayColor.a * u_overlayOpacity);
        }
    }
    
    if (u_hasHighlight && u_highlightColor.a > 0.0) {
        mapColor = mix(mapColor, u_highlightColor, 0.3);
    }
    
    outColor = mapColor;
}
`;

// Border line shader
const BORDER_VERTEX_SHADER = `#version 300 es
precision highp float;

in vec2 a_position;
uniform vec2 u_resolution;
uniform vec2 u_translation;
uniform float u_scale;

void main() {
    vec2 position = (a_position * u_scale + u_translation) / u_resolution * 2.0 - 1.0;
    position.y = -position.y;
    gl_Position = vec4(position, 0, 1);
}
`;

const BORDER_FRAGMENT_SHADER = `#version 300 es
precision highp float;

out vec4 outColor;
uniform vec4 u_color;

void main() {
    outColor = u_color;
}
`;

// Grid shader
const GRID_VERTEX_SHADER = `#version 300 es
precision highp float;

in vec2 a_position;

uniform vec2 u_resolution;
uniform vec2 u_translation;
uniform float u_scale;

void main() {
    vec2 position = (a_position * u_scale + u_translation) / u_resolution * 2.0 - 1.0;
    position.y = -position.y;
    gl_Position = vec4(position, 0, 1);
}
`;

const GRID_FRAGMENT_SHADER = `#version 300 es
precision highp float;

out vec4 outColor;
uniform vec4 u_gridColor;

void main() {
    outColor = u_gridColor;
}
`;

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

export class WebGLRenderer {
  private canvas: HTMLCanvasElement;
  private gl: WebGL2RenderingContext;
  
  // Main shader program
  private mainProgram: WebGLProgram;
  private mainVAO: WebGLVertexArrayObject;
  private positionBuffer: WebGLBuffer;
  private texCoordBuffer: WebGLBuffer;
  
  // Border shader program
  private borderProgram: WebGLProgram;
  private borderVAO: WebGLVertexArrayObject;
  private borderBuffer: WebGLBuffer;
  
  // Grid shader program
  private gridProgram: WebGLProgram;
  private gridVAO: WebGLVertexArrayObject;
  private gridBuffer: WebGLBuffer;
  
  // Textures
  private mapTexture: WebGLTexture;
  private overlayTexture: WebGLTexture;
  
  // Map dimensions
  private mapWidth: number = 0;
  private mapHeight: number = 0;
  
  // Cached border data
  private stateBorders: Map<number, BorderSegment> = new Map();
  private strategicRegionBorders: Map<number, BorderSegment> = new Map();
  private aiAreaBorders: Map<string, BorderSegment> = new Map();
  
  // Province pixel lookup (for selection highlighting)
  private provincePixelData: Uint8Array | null = null;
  private highlightMask: Uint8Array | null = null;

  constructor(canvas: HTMLCanvasElement) {
    this.canvas = canvas;
    
    const gl = canvas.getContext('webgl2', {
      alpha: false,
      antialias: false,
      preserveDrawingBuffer: true,
      powerPreference: 'high-performance',
    });
    
    if (!gl) {
      throw new Error('WebGL2 is not supported');
    }
    
    this.gl = gl;
    
    // Create shader programs
    this.mainProgram = this.createProgram(VERTEX_SHADER_SOURCE, FRAGMENT_SHADER_SOURCE);
    this.borderProgram = this.createProgram(BORDER_VERTEX_SHADER, BORDER_FRAGMENT_SHADER);
    this.gridProgram = this.createProgram(GRID_VERTEX_SHADER, GRID_FRAGMENT_SHADER);
    
    // Create VAOs and buffers
    this.mainVAO = this.createMainVAO();
    this.positionBuffer = gl.createBuffer()!;
    this.texCoordBuffer = gl.createBuffer()!;
    
    this.borderVAO = gl.createVertexArray()!;
    this.borderBuffer = gl.createBuffer()!;
    this.setupBorderVAO();
    
    this.gridVAO = gl.createVertexArray()!;
    this.gridBuffer = gl.createBuffer()!;
    this.setupGridVAO();
    
    // Create textures
    this.mapTexture = this.createTexture();
    this.overlayTexture = this.createTexture();
    
    // Enable blending
    gl.enable(gl.BLEND);
    gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
  }

  private createShader(type: number, source: string): WebGLShader {
    const { gl } = this;
    const shader = gl.createShader(type)!;
    gl.shaderSource(shader, source);
    gl.compileShader(shader);
    
    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
      const error = gl.getShaderInfoLog(shader);
      gl.deleteShader(shader);
      throw new Error(`Shader compilation failed: ${error}`);
    }
    
    return shader;
  }

  private createProgram(vertexSource: string, fragmentSource: string): WebGLProgram {
    const { gl } = this;
    const vertexShader = this.createShader(gl.VERTEX_SHADER, vertexSource);
    const fragmentShader = this.createShader(gl.FRAGMENT_SHADER, fragmentSource);
    
    const program = gl.createProgram()!;
    gl.attachShader(program, vertexShader);
    gl.attachShader(program, fragmentShader);
    gl.linkProgram(program);
    
    if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
      const error = gl.getProgramInfoLog(program);
      gl.deleteProgram(program);
      throw new Error(`Program linking failed: ${error}`);
    }
    
    gl.deleteShader(vertexShader);
    gl.deleteShader(fragmentShader);
    
    return program;
  }

  private createMainVAO(): WebGLVertexArrayObject {
    const { gl } = this;
    const vao = gl.createVertexArray()!;
    
    // Create buffers first
    this.positionBuffer = gl.createBuffer()!;
    this.texCoordBuffer = gl.createBuffer()!;
    
    // Initialize buffers with empty data
    gl.bindBuffer(gl.ARRAY_BUFFER, this.positionBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(12), gl.DYNAMIC_DRAW);
    
    gl.bindBuffer(gl.ARRAY_BUFFER, this.texCoordBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(12), gl.DYNAMIC_DRAW);
    
    // Now setup VAO
    gl.bindVertexArray(vao);
    
    // Position attribute
    const positionLocation = gl.getAttribLocation(this.mainProgram, 'a_position');
    gl.bindBuffer(gl.ARRAY_BUFFER, this.positionBuffer);
    gl.enableVertexAttribArray(positionLocation);
    gl.vertexAttribPointer(positionLocation, 2, gl.FLOAT, false, 0, 0);
    
    // Texture coordinate attribute
    const texCoordLocation = gl.getAttribLocation(this.mainProgram, 'a_texCoord');
    gl.bindBuffer(gl.ARRAY_BUFFER, this.texCoordBuffer);
    gl.enableVertexAttribArray(texCoordLocation);
    gl.vertexAttribPointer(texCoordLocation, 2, gl.FLOAT, false, 0, 0);
    
    gl.bindVertexArray(null);
    return vao;
  }

  private setupBorderVAO(): void {
    const { gl } = this;
    gl.bindVertexArray(this.borderVAO);
    gl.bindBuffer(gl.ARRAY_BUFFER, this.borderBuffer);
    
    const positionLocation = gl.getAttribLocation(this.borderProgram, 'a_position');
    gl.enableVertexAttribArray(positionLocation);
    gl.vertexAttribPointer(positionLocation, 2, gl.FLOAT, false, 0, 0);
    
    gl.bindVertexArray(null);
  }

  private setupGridVAO(): void {
    const { gl } = this;
    gl.bindVertexArray(this.gridVAO);
    gl.bindBuffer(gl.ARRAY_BUFFER, this.gridBuffer);
    
    const positionLocation = gl.getAttribLocation(this.gridProgram, 'a_position');
    gl.enableVertexAttribArray(positionLocation);
    gl.vertexAttribPointer(positionLocation, 2, gl.FLOAT, false, 0, 0);
    
    gl.bindVertexArray(null);
  }

  private createTexture(): WebGLTexture {
    const { gl } = this;
    const texture = gl.createTexture()!;
    gl.bindTexture(gl.TEXTURE_2D, texture);
    
    // Set texture parameters for pixel-perfect rendering
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.NEAREST);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST);
    
    return texture;
  }

  /**
   * Upload map pixel data to GPU texture
   */
  uploadMapData(pixels: Uint8Array, width: number, height: number): void {
    const { gl } = this;
    
    this.mapWidth = width;
    this.mapHeight = height;
    this.provincePixelData = new Uint8Array(pixels);
    
    // Convert RGB to RGBA
    const rgbaData = new Uint8Array(width * height * 4);
    for (let i = 0; i < width * height; i++) {
      rgbaData[i * 4] = pixels[i * 3];
      rgbaData[i * 4 + 1] = pixels[i * 3 + 1];
      rgbaData[i * 4 + 2] = pixels[i * 3 + 2];
      rgbaData[i * 4 + 3] = 255;
    }
    
    gl.bindTexture(gl.TEXTURE_2D, this.mapTexture);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, width, height, 0, gl.RGBA, gl.UNSIGNED_BYTE, rgbaData);
    
    // Initialize highlight mask
    this.highlightMask = new Uint8Array(width * height * 4);
    
    // Update quad vertices
    this.updateQuadVertices();
  }

  /**
   * Update map texture from modified pixel data
   */
  updateMapTexture(pixels: Uint8Array): void {
    const { gl } = this;
    
    if (!this.mapWidth || !this.mapHeight) return;
    
    this.provincePixelData = new Uint8Array(pixels);
    
    // Convert RGB to RGBA
    const rgbaData = new Uint8Array(this.mapWidth * this.mapHeight * 4);
    for (let i = 0; i < this.mapWidth * this.mapHeight; i++) {
      rgbaData[i * 4] = pixels[i * 3];
      rgbaData[i * 4 + 1] = pixels[i * 3 + 1];
      rgbaData[i * 4 + 2] = pixels[i * 3 + 2];
      rgbaData[i * 4 + 3] = 255;
    }
    
    gl.bindTexture(gl.TEXTURE_2D, this.mapTexture);
    gl.texSubImage2D(gl.TEXTURE_2D, 0, 0, 0, this.mapWidth, this.mapHeight, gl.RGBA, gl.UNSIGNED_BYTE, rgbaData);
  }

  private updateQuadVertices(): void {
    const { gl } = this;
    
    // Position vertices (full quad - two triangles)
    const positions = new Float32Array([
      0, 0,
      this.mapWidth, 0,
      0, this.mapHeight,
      0, this.mapHeight,
      this.mapWidth, 0,
      this.mapWidth, this.mapHeight,
    ]);
    
    gl.bindBuffer(gl.ARRAY_BUFFER, this.positionBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, positions, gl.STATIC_DRAW);
    
    // Texture coordinates (matching position order)
    const texCoords = new Float32Array([
      0, 0,  // top-left
      1, 0,  // top-right
      0, 1,  // bottom-left
      0, 1,  // bottom-left
      1, 0,  // top-right
      1, 1,  // bottom-right
    ]);
    
    gl.bindBuffer(gl.ARRAY_BUFFER, this.texCoordBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, texCoords, gl.STATIC_DRAW);
  }

  /**
   * Generate border segments for states
   */
  generateStateBorders(
    states: Map<number, State>,
    provinces: Map<number, Province>,
    provinceByColor: Map<string, Province>
  ): void {
    this.stateBorders.clear();
    
    // Create province to state mapping
    const provinceToState = new Map<number, number>();
    for (const [stateId, state] of states) {
      for (const provinceId of state.provinces) {
        provinceToState.set(provinceId, stateId);
      }
    }
    
    // Generate borders by detecting state boundaries in pixel data
    if (!this.provincePixelData) return;
    
    const borderPixels = this.detectBorders(
      provinces,
      provinceByColor,
      (p1, p2) => provinceToState.get(p1?.id ?? -1) !== provinceToState.get(p2?.id ?? -1)
    );
    
    // Group by state and create border segments
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
          color: [1.0, 0.8, 0.0, 0.8], // Yellow for state borders
        });
      }
    }
  }

  /**
   * Generate border segments for strategic regions
   */
  generateStrategicRegionBorders(
    regions: Map<number, StrategicRegion>,
    provinces: Map<number, Province>,
    provinceByColor: Map<string, Province>
  ): void {
    this.strategicRegionBorders.clear();
    
    // Create province to region mapping
    const provinceToRegion = new Map<number, number>();
    for (const [regionId, region] of regions) {
      for (const provinceId of region.provinces) {
        provinceToRegion.set(provinceId, regionId);
      }
    }
    
    if (!this.provincePixelData) return;
    
    const borderPixels = this.detectBorders(
      provinces,
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
          color: [0.0, 0.8, 1.0, 0.8], // Cyan for strategic region borders
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
    provinces: Map<number, Province>,
    provinceByColor: Map<string, Province>
  ): void {
    this.aiAreaBorders.clear();
    
    // Build province to AI area mapping
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
      provinces,
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
          color: [1.0, 0.0, 0.8, 0.8], // Magenta for AI area borders
        });
      }
    }
  }

  private detectBorders(
    _provinces: Map<number, Province>,
    provinceByColor: Map<string, Province>,
    isBoundary: (p1: Province | undefined, p2: Province | undefined) => boolean
  ): [number, number][] {
    const borderPixels: [number, number][] = [];
    
    if (!this.provincePixelData) return borderPixels;
    
    const width = this.mapWidth;
    const height = this.mapHeight;
    
    // Sample at lower resolution for performance
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
   * Create highlight overlay for selected/hovered province
   */
  updateHighlightOverlay(
    selectedProvinceId: number | null,
    hoveredProvinceId: number | null,
    provinces: Map<number, Province>
  ): void {
    const { gl } = this;
    
    if (!this.highlightMask || !this.provincePixelData) return;
    
    // Clear highlight mask
    this.highlightMask.fill(0);
    
    const selectedProvince = selectedProvinceId ? provinces.get(selectedProvinceId) : null;
    const hoveredProvince = hoveredProvinceId ? provinces.get(hoveredProvinceId) : null;
    
    // Apply highlights
    for (let i = 0; i < this.mapWidth * this.mapHeight; i++) {
      const r = this.provincePixelData[i * 3];
      const g = this.provincePixelData[i * 3 + 1];
      const b = this.provincePixelData[i * 3 + 2];
      
      if (selectedProvince && 
          r === selectedProvince.color.r &&
          g === selectedProvince.color.g &&
          b === selectedProvince.color.b) {
        // Yellow highlight for selected
        this.highlightMask[i * 4] = 255;
        this.highlightMask[i * 4 + 1] = 200;
        this.highlightMask[i * 4 + 2] = 0;
        this.highlightMask[i * 4 + 3] = 128;
      } else if (hoveredProvince && 
                 r === hoveredProvince.color.r &&
                 g === hoveredProvince.color.g &&
                 b === hoveredProvince.color.b) {
        // Light blue highlight for hovered
        this.highlightMask[i * 4] = 100;
        this.highlightMask[i * 4 + 1] = 200;
        this.highlightMask[i * 4 + 2] = 255;
        this.highlightMask[i * 4 + 3] = 80;
      }
    }
    
    // Upload to texture
    gl.bindTexture(gl.TEXTURE_2D, this.overlayTexture);
    gl.texImage2D(
      gl.TEXTURE_2D, 0, gl.RGBA,
      this.mapWidth, this.mapHeight, 0,
      gl.RGBA, gl.UNSIGNED_BYTE, this.highlightMask
    );
  }

  /**
   * Render the map with all overlays
   */
  render(state: RenderState): void {
    const { gl } = this;
    
    // Resize canvas if needed
    if (this.canvas.width !== state.viewportWidth || this.canvas.height !== state.viewportHeight) {
      this.canvas.width = state.viewportWidth;
      this.canvas.height = state.viewportHeight;
      gl.viewport(0, 0, state.viewportWidth, state.viewportHeight);
    }
    
    // Clear canvas
    gl.clearColor(0.12, 0.12, 0.12, 1.0);
    gl.clear(gl.COLOR_BUFFER_BIT);
    
    if (!this.mapWidth || !this.mapHeight) return;
    
    // Render main map
    gl.useProgram(this.mainProgram);
    gl.bindVertexArray(this.mainVAO);
    
    // Set uniforms
    const resolutionLocation = gl.getUniformLocation(this.mainProgram, 'u_resolution');
    const translationLocation = gl.getUniformLocation(this.mainProgram, 'u_translation');
    const scaleLocation = gl.getUniformLocation(this.mainProgram, 'u_scale');
    const mapTextureLocation = gl.getUniformLocation(this.mainProgram, 'u_mapTexture');
    const overlayTextureLocation = gl.getUniformLocation(this.mainProgram, 'u_overlayTexture');
    const overlayOpacityLocation = gl.getUniformLocation(this.mainProgram, 'u_overlayOpacity');
    const hasOverlayLocation = gl.getUniformLocation(this.mainProgram, 'u_hasOverlay');
    
    gl.uniform2f(resolutionLocation, state.viewportWidth, state.viewportHeight);
    gl.uniform2f(translationLocation, state.panX, state.panY);
    gl.uniform1f(scaleLocation, state.zoom);
    
    // Bind textures
    gl.activeTexture(gl.TEXTURE0);
    gl.bindTexture(gl.TEXTURE_2D, this.mapTexture);
    gl.uniform1i(mapTextureLocation, 0);
    
    gl.activeTexture(gl.TEXTURE1);
    gl.bindTexture(gl.TEXTURE_2D, this.overlayTexture);
    gl.uniform1i(overlayTextureLocation, 1);
    
    gl.uniform1f(overlayOpacityLocation, state.layerOpacity);
    gl.uniform1i(hasOverlayLocation, 
      state.selectedProvinceId !== null || state.hoveredProvinceId !== null ? 1 : 0
    );
    
    // Draw map quad
    gl.drawArrays(gl.TRIANGLES, 0, 6);
    
    // Render borders based on active layer
    if (state.showBorders) {
      this.renderBorders(state);
    }
    
    // Render grid at high zoom
    if (state.showGrid && state.zoom >= 8) {
      this.renderGrid(state);
    }
    
    gl.bindVertexArray(null);
  }

  private renderBorders(state: RenderState): void {
    const { gl } = this;
    
    gl.useProgram(this.borderProgram);
    gl.bindVertexArray(this.borderVAO);
    
    const resolutionLocation = gl.getUniformLocation(this.borderProgram, 'u_resolution');
    const translationLocation = gl.getUniformLocation(this.borderProgram, 'u_translation');
    const scaleLocation = gl.getUniformLocation(this.borderProgram, 'u_scale');
    const colorLocation = gl.getUniformLocation(this.borderProgram, 'u_color');
    
    gl.uniform2f(resolutionLocation, state.viewportWidth, state.viewportHeight);
    gl.uniform2f(translationLocation, state.panX, state.panY);
    gl.uniform1f(scaleLocation, state.zoom);
    
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
    
    for (const [, segment] of borders) {
      gl.uniform4fv(colorLocation, segment.color);
      gl.bindBuffer(gl.ARRAY_BUFFER, this.borderBuffer);
      gl.bufferData(gl.ARRAY_BUFFER, segment.points, gl.DYNAMIC_DRAW);
      gl.drawArrays(gl.POINTS, 0, segment.points.length / 2);
    }
    
    gl.bindVertexArray(null);
  }

  private renderGrid(state: RenderState): void {
    const { gl } = this;
    
    gl.useProgram(this.gridProgram);
    gl.bindVertexArray(this.gridVAO);
    
    const resolutionLocation = gl.getUniformLocation(this.gridProgram, 'u_resolution');
    const translationLocation = gl.getUniformLocation(this.gridProgram, 'u_translation');
    const scaleLocation = gl.getUniformLocation(this.gridProgram, 'u_scale');
    const gridColorLocation = gl.getUniformLocation(this.gridProgram, 'u_gridColor');
    
    gl.uniform2f(resolutionLocation, state.viewportWidth, state.viewportHeight);
    gl.uniform2f(translationLocation, state.panX, state.panY);
    gl.uniform1f(scaleLocation, state.zoom);
    gl.uniform4f(gridColorLocation, 0.4, 0.4, 0.4, 0.3);
    
    // Calculate visible area
    const startX = Math.max(0, Math.floor(-state.panX / state.zoom));
    const startY = Math.max(0, Math.floor(-state.panY / state.zoom));
    const endX = Math.min(this.mapWidth, Math.ceil((state.viewportWidth - state.panX) / state.zoom));
    const endY = Math.min(this.mapHeight, Math.ceil((state.viewportHeight - state.panY) / state.zoom));
    
    // Generate grid lines
    const gridLines: number[] = [];
    
    for (let x = startX; x <= endX; x++) {
      gridLines.push(x, startY, x, endY);
    }
    for (let y = startY; y <= endY; y++) {
      gridLines.push(startX, y, endX, y);
    }
    
    gl.bindBuffer(gl.ARRAY_BUFFER, this.gridBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(gridLines), gl.DYNAMIC_DRAW);
    gl.drawArrays(gl.LINES, 0, gridLines.length / 2);
    
    gl.bindVertexArray(null);
  }

  /**
   * Resize the renderer viewport
   */
  resize(width: number, height: number): void {
    this.canvas.width = width;
    this.canvas.height = height;
    this.gl.viewport(0, 0, width, height);
  }

  /**
   * Get map dimensions
   */
  getMapDimensions(): { width: number; height: number } {
    return { width: this.mapWidth, height: this.mapHeight };
  }

  /**
   * Cleanup WebGL resources
   */
  dispose(): void {
    const { gl } = this;
    
    gl.deleteProgram(this.mainProgram);
    gl.deleteProgram(this.borderProgram);
    gl.deleteProgram(this.gridProgram);
    
    gl.deleteBuffer(this.positionBuffer);
    gl.deleteBuffer(this.texCoordBuffer);
    gl.deleteBuffer(this.borderBuffer);
    gl.deleteBuffer(this.gridBuffer);
    
    gl.deleteVertexArray(this.mainVAO);
    gl.deleteVertexArray(this.borderVAO);
    gl.deleteVertexArray(this.gridVAO);
    
    gl.deleteTexture(this.mapTexture);
    gl.deleteTexture(this.overlayTexture);
  }
}
