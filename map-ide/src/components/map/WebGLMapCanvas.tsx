/**
 * WebGL-based Map Canvas component
 * High-performance rendering with layer overlays for states, strategic regions, and AI areas
 */

import React, { useRef, useEffect, useCallback, useState, useMemo } from 'react';
import { useMapStore } from '../../stores/mapStore';
import { useProjectStore } from '../../stores/projectStore';
import { useSettingsStore } from '../../stores/settingsStore';
import { WebGLRenderer, RenderState } from '../../core/WebGLRenderer';
import { rgbToKey } from '../../utils/colorUtils';
import {
  buildStateAdjacency,
  buildStrategicRegionAdjacency,
  buildAIAreaAdjacency,
  generateStateColors,
  generateStrategicRegionColors,
  generateAIAreaColors,
  createLayerOverlay,
} from '../../utils/layerColors';
import { RGB } from '../../types';

interface MouseState {
  isDragging: boolean;
  isDrawing: boolean;
  lastPos: { x: number; y: number } | null;
  lineStart: { x: number; y: number } | null;
}

const WebGLMapCanvas: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const rendererRef = useRef<WebGLRenderer | null>(null);
  const animationFrameRef = useRef<number>(0);
  
  const [mouseState, setMouseState] = useState<MouseState>({
    isDragging: false,
    isDrawing: false,
    lastPos: null,
    lineStart: null,
  });
  
  const [rendererType, setRendererType] = useState<'webgl' | 'canvas2d' | 'none'>('none');
  const [rendererReady, setRendererReady] = useState(false);
  const [debugInfo, setDebugInfo] = useState<string>('');
  
  // Layer color caches
  const [stateColors, setStateColors] = useState<Map<number, RGB>>(new Map());
  const [regionColors, setRegionColors] = useState<Map<number, RGB>>(new Map());
  const [aiAreaColors, setAIAreaColors] = useState<Map<string, RGB>>(new Map());
  const [layerOverlay, setLayerOverlay] = useState<Uint8Array | null>(null);
  
  // i18n
  const t = useSettingsStore((state) => state.t);

  // Map store state
  const bmpEditor = useMapStore((state) => state.bmpEditor);
  const zoom = useMapStore((state) => state.zoom);
  const panX = useMapStore((state) => state.panX);
  const panY = useMapStore((state) => state.panY);
  const viewportWidth = useMapStore((state) => state.viewportWidth);
  const viewportHeight = useMapStore((state) => state.viewportHeight);
  const setPan = useMapStore((state) => state.setPan);
  const setZoom = useMapStore((state) => state.setZoom);
  const setViewport = useMapStore((state) => state.setViewport);
  const fitToView = useMapStore((state) => state.fitToView);
  const activeTool = useMapStore((state) => state.activeTool);
  const selectedColor = useMapStore((state) => state.selectedColor);
  const showGrid = useMapStore((state) => state.showGrid);
  const showBorders = useMapStore((state) => state.showBorders);
  const layers = useMapStore((state) => state.layers);
  const selectedProvinceId = useMapStore((state) => state.selectedProvinceId);
  const hoveredProvinceId = useMapStore((state) => state.hoveredProvinceId);
  const applyBrush = useMapStore((state) => state.applyBrush);
  const applyFill = useMapStore((state) => state.applyFill);
  const applyLine = useMapStore((state) => state.applyLine);
  const applyRect = useMapStore((state) => state.applyRect);
  const pickColor = useMapStore((state) => state.pickColor);
  const commitChanges = useMapStore((state) => state.commitChanges);
  const selectProvince = useMapStore((state) => state.selectProvince);
  const setHoveredProvince = useMapStore((state) => state.setHoveredProvince);

  // Project store state
  const provinces = useProjectStore((state) => state.provinces);
  const provinceByColor = useProjectStore((state) => state.provinceByColor);
  const states = useProjectStore((state) => state.states);
  const strategicRegions = useProjectStore((state) => state.strategicRegions);
  const aiAreas = useProjectStore((state) => state.aiAreas);

  // Determine active layer
  const activeLayer = useMemo(() => {
    if (layers.aiAreas) return 'aiAreas' as const;
    if (layers.strategicRegions) return 'strategicRegions' as const;
    if (layers.states) return 'states' as const;
    return 'provinces' as const;
  }, [layers]);

  // Initialize WebGL renderer
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) {
      console.log('[WebGLMapCanvas] Canvas ref not ready yet');
      return;
    }

    // Check if renderer already exists
    if (rendererRef.current) {
      console.log('[WebGLMapCanvas] Renderer already exists');
      return;
    }

    try {
      console.log('[WebGLMapCanvas] Creating WebGLRenderer...');
      rendererRef.current = new WebGLRenderer(canvas);
      const type = rendererRef.current.getRendererType();
      setRendererType(type);
      setRendererReady(true);
      console.log('[WebGLMapCanvas] Renderer initialized:', type);
    } catch (error) {
      console.error('[WebGLMapCanvas] Failed to initialize renderer:', error);
      setRendererType('none');
      setRendererReady(false);
    }

    return () => {
      console.log('[WebGLMapCanvas] Disposing renderer');
      rendererRef.current?.dispose();
      rendererRef.current = null;
      setRendererReady(false);
    };
  }, []);

  // Upload map data to GPU when BMP editor changes AND renderer is ready
  useEffect(() => {
    console.log('[WebGLMapCanvas] Upload effect triggered - rendererReady:', rendererReady, 'bmpEditor:', !!bmpEditor);
    
    if (!rendererReady) {
      setDebugInfo('Waiting for renderer...');
      return;
    }
    
    const renderer = rendererRef.current;
    if (!renderer) {
      setDebugInfo('Renderer ref is null');
      return;
    }
    
    if (!bmpEditor) {
      setDebugInfo('Waiting for BMP data...');
      return;
    }

    console.log('[WebGLMapCanvas] Uploading map data:', bmpEditor.width, 'x', bmpEditor.height);
    setDebugInfo(`Map: ${bmpEditor.width}x${bmpEditor.height}`);
    renderer.uploadMapData(bmpEditor.pixels, bmpEditor.width, bmpEditor.height);
    
    // Fit to view after loading
    setTimeout(fitToView, 100);
  }, [bmpEditor, rendererReady, fitToView]);

  // Update map texture when pixels change
  useEffect(() => {
    const renderer = rendererRef.current;
    if (!renderer || !bmpEditor) return;

    renderer.updateMapTexture(bmpEditor.pixels);
  }, [bmpEditor?.pixels]);

  // Generate borders and layer colors when data changes
  useEffect(() => {
    const renderer = rendererRef.current;
    if (!renderer || !bmpEditor || provinces.size === 0) return;

    console.log('[WebGLMapCanvas] Generating borders and colors...');

    // Build adjacency graphs and generate colors
    if (states.size > 0) {
      // Generate state borders
      renderer.generateStateBorders(states, provinces, provinceByColor);
      
      // Build state adjacency and colors
      const stateAdj = buildStateAdjacency(
        states, provinces, bmpEditor.pixels, bmpEditor.width, bmpEditor.height, provinceByColor
      );
      const colors = generateStateColors(states, stateAdj);
      setStateColors(colors);
      console.log('[WebGLMapCanvas] Generated colors for', colors.size, 'states');
      
      // Build strategic region adjacency based on state adjacency
      if (strategicRegions.size > 0) {
        renderer.generateStrategicRegionBorders(strategicRegions, provinces, provinceByColor);
        
        const regionAdj = buildStrategicRegionAdjacency(strategicRegions, states, stateAdj);
        const rColors = generateStrategicRegionColors(strategicRegions, regionAdj);
        setRegionColors(rColors);
        console.log('[WebGLMapCanvas] Generated colors for', rColors.size, 'strategic regions');
        
        // Build AI area adjacency based on region adjacency
        if (aiAreas.length > 0) {
          renderer.generateAIAreaBorders(aiAreas, strategicRegions, provinces, provinceByColor);
          
          const aiAdj = buildAIAreaAdjacency(aiAreas, regionAdj);
          const aColors = generateAIAreaColors(aiAreas, aiAdj);
          setAIAreaColors(aColors);
          console.log('[WebGLMapCanvas] Generated colors for', aColors.size, 'AI areas');
        }
      }
    } else {
      // Generate strategic region borders even without states
      if (strategicRegions.size > 0) {
        renderer.generateStrategicRegionBorders(strategicRegions, provinces, provinceByColor);
      }

      // Generate AI area borders
      if (aiAreas.length > 0) {
        renderer.generateAIAreaBorders(aiAreas, strategicRegions, provinces, provinceByColor);
      }
    }
  }, [bmpEditor, provinces, provinceByColor, states, strategicRegions, aiAreas]);

  // Generate layer overlay when active layer or colors change
  useEffect(() => {
    if (!bmpEditor || provinces.size === 0) {
      setLayerOverlay(null);
      return;
    }

    let overlay: Uint8Array | null = null;
    let provinceToEntity: Map<number, number | string> | null = null;
    let entityColors: Map<number | string, RGB> | null = null;

    if (activeLayer === 'states' && stateColors.size > 0) {
      // Map provinces to states
      provinceToEntity = new Map();
      for (const [stateId, state] of states) {
        for (const provId of state.provinces) {
          provinceToEntity.set(provId, stateId);
        }
      }
      entityColors = stateColors as Map<number | string, RGB>;
    } else if (activeLayer === 'strategicRegions' && regionColors.size > 0) {
      // Map provinces to regions
      provinceToEntity = new Map();
      for (const [regionId, region] of strategicRegions) {
        for (const provId of region.provinces) {
          provinceToEntity.set(provId, regionId);
        }
      }
      entityColors = regionColors as Map<number | string, RGB>;
    } else if (activeLayer === 'aiAreas' && aiAreaColors.size > 0) {
      // Map provinces to AI areas via regions
      provinceToEntity = new Map();
      for (const area of aiAreas) {
        if (area.strategicRegions) {
          for (const regionId of area.strategicRegions) {
            const region = strategicRegions.get(regionId);
            if (region) {
              for (const provId of region.provinces) {
                provinceToEntity.set(provId, area.name);
              }
            }
          }
        }
      }
      entityColors = aiAreaColors as Map<number | string, RGB>;
    }

    if (provinceToEntity && entityColors && provinceToEntity.size > 0 && entityColors.size > 0) {
      overlay = createLayerOverlay(
        bmpEditor.width,
        bmpEditor.height,
        bmpEditor.pixels,
        provinceByColor,
        provinceToEntity,
        entityColors,
        0.6 // opacity
      );
      console.log('[WebGLMapCanvas] Created layer overlay for', activeLayer);
    }

    setLayerOverlay(overlay);

    // Upload to renderer
    const renderer = rendererRef.current;
    if (renderer) {
      renderer.uploadLayerOverlay(overlay);
    }
  }, [activeLayer, bmpEditor, provinces, provinceByColor, states, strategicRegions, aiAreas,
      stateColors, regionColors, aiAreaColors]);

  // Update highlight overlay
  useEffect(() => {
    const renderer = rendererRef.current;
    if (!renderer) return;

    renderer.updateHighlightOverlay(selectedProvinceId, hoveredProvinceId, provinces);
  }, [selectedProvinceId, hoveredProvinceId, provinces]);

  // Handle container resize
  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const resizeObserver = new ResizeObserver((entries) => {
      for (const entry of entries) {
        const { width, height } = entry.contentRect;
        setViewport(width, height);
        rendererRef.current?.resize(width, height);
      }
    });

    resizeObserver.observe(container);
    return () => resizeObserver.disconnect();
  }, [setViewport]);

  // Animation loop
  useEffect(() => {
    const render = () => {
      const renderer = rendererRef.current;
      if (renderer) {
        const renderState: RenderState = {
          zoom,
          panX,
          panY,
          viewportWidth,
          viewportHeight,
          showGrid,
          showBorders,
          selectedProvinceId,
          hoveredProvinceId,
          activeLayer,
          layerOpacity: 0.6,
          layerOverlay,
        };
        renderer.render(renderState);
      }
      animationFrameRef.current = requestAnimationFrame(render);
    };

    animationFrameRef.current = requestAnimationFrame(render);
    return () => cancelAnimationFrame(animationFrameRef.current);
  }, [zoom, panX, panY, viewportWidth, viewportHeight, showGrid, showBorders, 
      selectedProvinceId, hoveredProvinceId, activeLayer, layerOverlay]);

  // Convert screen coordinates to image coordinates
  const screenToImage = useCallback(
    (screenX: number, screenY: number) => {
      const rect = canvasRef.current?.getBoundingClientRect();
      if (!rect) return { x: 0, y: 0 };
      
      const x = (screenX - rect.left - panX) / zoom;
      const y = (screenY - rect.top - panY) / zoom;
      return { x, y };
    },
    [panX, panY, zoom]
  );

  // Get province at position
  const getProvinceAt = useCallback(
    (x: number, y: number) => {
      if (!bmpEditor) return null;
      try {
        const color = bmpEditor.getPixel(Math.floor(x), Math.floor(y));
        const key = rgbToKey(color);
        return provinceByColor.get(key) || null;
      } catch {
        return null;
      }
    },
    [bmpEditor, provinceByColor]
  );

  // Mouse handlers
  const handleMouseDown = useCallback(
    (e: React.MouseEvent) => {
      if (e.button === 1 || (e.button === 0 && e.altKey)) {
        // Middle button or Alt+Left: Pan
        setMouseState((prev) => ({
          ...prev,
          isDragging: true,
          lastPos: { x: e.clientX, y: e.clientY },
        }));
        return;
      }

      if (e.button !== 0) return;

      const pos = screenToImage(e.clientX, e.clientY);

      switch (activeTool) {
        case 'select': {
          const province = getProvinceAt(pos.x, pos.y);
          selectProvince(province?.id || null);
          break;
        }

        case 'brush':
        case 'pencil':
        case 'eraser':
          if (selectedColor || activeTool === 'eraser') {
            setMouseState((prev) => ({ ...prev, isDrawing: true }));
            applyBrush(pos.x, pos.y);
          }
          break;

        case 'fill':
          if (selectedColor) {
            applyFill(pos.x, pos.y);
          }
          break;

        case 'eyedropper':
          pickColor(pos.x, pos.y);
          break;

        case 'line':
        case 'rectangle':
          setMouseState((prev) => ({
            ...prev,
            lineStart: pos,
            lastPos: pos,
          }));
          break;
      }
    },
    [activeTool, selectedColor, screenToImage, getProvinceAt, selectProvince, applyBrush, applyFill, pickColor]
  );

  const handleMouseMove = useCallback(
    (e: React.MouseEvent) => {
      const pos = screenToImage(e.clientX, e.clientY);

      // Update hovered province
      const province = getProvinceAt(pos.x, pos.y);
      setHoveredProvince(province?.id || null);

      const { isDragging, isDrawing, lastPos, lineStart } = mouseState;

      if (isDragging && lastPos) {
        const dx = e.clientX - lastPos.x;
        const dy = e.clientY - lastPos.y;
        setPan(panX + dx, panY + dy);
        setMouseState((prev) => ({
          ...prev,
          lastPos: { x: e.clientX, y: e.clientY },
        }));
        return;
      }

      if (isDrawing && (activeTool === 'brush' || activeTool === 'pencil' || activeTool === 'eraser')) {
        applyBrush(pos.x, pos.y);
      }

      if (lineStart && (activeTool === 'line' || activeTool === 'rectangle')) {
        setMouseState((prev) => ({ ...prev, lastPos: pos }));
      }
    },
    [mouseState, activeTool, panX, panY, screenToImage, getProvinceAt, setHoveredProvince, setPan, applyBrush]
  );

  const handleMouseUp = useCallback(
    (e: React.MouseEvent) => {
      const { isDragging, isDrawing, lineStart } = mouseState;

      if (isDragging) {
        setMouseState((prev) => ({
          ...prev,
          isDragging: false,
          lastPos: null,
        }));
        return;
      }

      if (isDrawing) {
        commitChanges();
        setMouseState((prev) => ({ ...prev, isDrawing: false }));
      }

      if (lineStart && (activeTool === 'line' || activeTool === 'rectangle')) {
        const pos = screenToImage(e.clientX, e.clientY);
        
        if (selectedColor) {
          if (activeTool === 'line') {
            applyLine(lineStart.x, lineStart.y, pos.x, pos.y);
          } else {
            applyRect(lineStart.x, lineStart.y, pos.x, pos.y);
          }
        }
        
        setMouseState((prev) => ({
          ...prev,
          lineStart: null,
          lastPos: null,
        }));
      }
    },
    [mouseState, activeTool, selectedColor, screenToImage, commitChanges, applyLine, applyRect]
  );

  // Handle wheel event with native listener for passive: false
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const handleWheel = (e: WheelEvent) => {
      e.preventDefault();
      e.stopPropagation();

      const rect = canvas.getBoundingClientRect();

      // Get mouse position relative to canvas
      const mouseX = e.clientX - rect.left;
      const mouseY = e.clientY - rect.top;

      // Calculate zoom
      const zoomFactor = e.deltaY > 0 ? 0.9 : 1.1;
      const newZoom = Math.max(0.1, Math.min(32, zoom * zoomFactor));

      // Adjust pan to zoom towards mouse position
      const newPanX = mouseX - (mouseX - panX) * (newZoom / zoom);
      const newPanY = mouseY - (mouseY - panY) * (newZoom / zoom);

      setZoom(newZoom);
      setPan(newPanX, newPanY);
    };

    // Add with passive: false to allow preventDefault
    canvas.addEventListener('wheel', handleWheel, { passive: false });
    return () => canvas.removeEventListener('wheel', handleWheel);
  }, [zoom, panX, panY, setZoom, setPan]);

  const handleMouseLeave = useCallback(() => {
    setMouseState({
      isDragging: false,
      isDrawing: false,
      lastPos: null,
      lineStart: null,
    });
    setHoveredProvince(null);
  }, [setHoveredProvince]);

  // Cursor style based on tool
  const getCursor = () => {
    switch (activeTool) {
      case 'select':
        return 'default';
      case 'brush':
      case 'pencil':
        return 'crosshair';
      case 'fill':
        return 'cell';
      case 'eyedropper':
        return 'copy';
      case 'eraser':
        return 'crosshair';
      case 'line':
      case 'rectangle':
        return 'crosshair';
      default:
        return 'default';
    }
  };

  return (
    <div
      ref={containerRef}
      className="flex-1 overflow-hidden bg-ide-bg relative"
      style={{ cursor: getCursor() }}
    >
      {/* Canvas is always rendered so ref is available for WebGL initialization */}
      <canvas
        ref={canvasRef}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseLeave}
        onContextMenu={(e) => e.preventDefault()}
        className="w-full h-full"
        style={{ display: bmpEditor ? 'block' : 'none' }}
      />
      
      {/* Loading overlay when no bmpEditor */}
      {!bmpEditor && (
        <div className="absolute inset-0 flex items-center justify-center bg-ide-bg text-ide-text-muted">
          <div className="text-center">
            <div className="text-6xl mb-4">🗺️</div>
            <div className="text-xl font-medium">{t.loadingMap}</div>
            <div className="text-sm mt-2 text-ide-text-muted">
              {t.welcomeDescription}
            </div>
          </div>
        </div>
      )}
      
      {/* Layer indicator */}
      <div className="absolute top-4 right-4 bg-ide-sidebar px-3 py-2 rounded-lg shadow-lg border border-ide-border">
        <div className="text-xs text-ide-text-muted mb-1">{t.activeLayer}</div>
        <div className="text-sm font-medium text-ide-text">
          {activeLayer === 'provinces' && `🟡 ${t.provinces}`}
          {activeLayer === 'states' && `🟠 ${t.states}`}
          {activeLayer === 'strategicRegions' && `🔵 ${t.strategicRegions}`}
          {activeLayer === 'aiAreas' && `🟣 ${t.aiAreas}`}
        </div>
      </div>
      
      {/* Zoom indicator */}
      <div className="absolute bottom-4 right-4 bg-ide-sidebar px-3 py-2 rounded-lg shadow-lg border border-ide-border">
        <div className="text-sm font-mono text-ide-text">
          {(zoom * 100).toFixed(0)}%
        </div>
        <div className="text-xs text-ide-text-muted mt-1">
          {rendererType === 'webgl' ? `🎮 ${t.webgl}` : rendererType === 'canvas2d' ? `🖌️ ${t.canvas}` : '⏳'}
        </div>
      </div>
      
      {/* Coordinate indicator */}
      {hoveredProvinceId && (
        <div className="absolute bottom-4 left-4 bg-ide-sidebar px-3 py-2 rounded-lg shadow-lg border border-ide-border">
          <div className="text-xs text-ide-text-muted">{t.provinceId}</div>
          <div className="text-sm font-mono text-ide-text">{hoveredProvinceId}</div>
        </div>
      )}
      
      {/* Debug info */}
      {debugInfo && (
        <div className="absolute top-4 left-4 bg-ide-sidebar px-3 py-2 rounded-lg shadow-lg border border-ide-border">
          <div className="text-xs text-ide-text-muted">Debug</div>
          <div className="text-xs font-mono text-ide-text">{debugInfo}</div>
        </div>
      )}
    </div>
  );
};

export default WebGLMapCanvas;
