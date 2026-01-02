import React, { useRef, useEffect, useCallback, useState } from 'react';
import { useMapStore } from '../../stores/mapStore';
import { useProjectStore } from '../../stores/projectStore';
import { pixelsToImageData } from '../../core/BMPParser';
import { rgbToKey } from '../../utils/colorUtils';

const MapCanvas: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  
  const [isDragging, setIsDragging] = useState(false);
  const [isDrawing, setIsDrawing] = useState(false);
  const [lastPos, setLastPos] = useState<{ x: number; y: number } | null>(null);
  const [lineStart, setLineStart] = useState<{ x: number; y: number } | null>(null);

  // Map store
  const bmpEditor = useMapStore((state) => state.bmpEditor);
  const zoom = useMapStore((state) => state.zoom);
  const panX = useMapStore((state) => state.panX);
  const panY = useMapStore((state) => state.panY);
  const setPan = useMapStore((state) => state.setPan);
  const setZoom = useMapStore((state) => state.setZoom);
  const setViewport = useMapStore((state) => state.setViewport);
  const fitToView = useMapStore((state) => state.fitToView);
  const activeTool = useMapStore((state) => state.activeTool);
  const selectedColor = useMapStore((state) => state.selectedColor);
  const showGrid = useMapStore((state) => state.showGrid);
  const applyBrush = useMapStore((state) => state.applyBrush);
  const applyFill = useMapStore((state) => state.applyFill);
  const applyLine = useMapStore((state) => state.applyLine);
  const applyRect = useMapStore((state) => state.applyRect);
  const pickColor = useMapStore((state) => state.pickColor);
  const commitChanges = useMapStore((state) => state.commitChanges);
  const selectProvince = useMapStore((state) => state.selectProvince);
  const setHoveredProvince = useMapStore((state) => state.setHoveredProvince);

  // Project store
  const provinceByColor = useProjectStore((state) => state.provinceByColor);

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

  // Render the map
  const render = useCallback(() => {
    const canvas = canvasRef.current;
    const ctx = canvas?.getContext('2d');
    if (!canvas || !ctx || !bmpEditor) return;

    // Clear canvas
    ctx.fillStyle = '#1e1e1e';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Save context
    ctx.save();

    // Apply pan and zoom
    ctx.translate(panX, panY);
    ctx.scale(zoom, zoom);

    // Draw BMP
    const imageData = pixelsToImageData(
      bmpEditor.pixels,
      bmpEditor.width,
      bmpEditor.height
    );
    
    // Create temp canvas for the image
    const tempCanvas = document.createElement('canvas');
    tempCanvas.width = bmpEditor.width;
    tempCanvas.height = bmpEditor.height;
    const tempCtx = tempCanvas.getContext('2d')!;
    tempCtx.putImageData(imageData, 0, 0);

    // Draw with image smoothing disabled for pixel-perfect rendering
    ctx.imageSmoothingEnabled = false;
    ctx.drawImage(tempCanvas, 0, 0);

    // Draw pixel grid at high zoom
    if (showGrid && zoom >= 8) {
      ctx.strokeStyle = 'rgba(100, 100, 100, 0.3)';
      ctx.lineWidth = 1 / zoom;

      // Calculate visible area
      const startX = Math.max(0, Math.floor(-panX / zoom));
      const startY = Math.max(0, Math.floor(-panY / zoom));
      const endX = Math.min(bmpEditor.width, Math.ceil((canvas.width - panX) / zoom));
      const endY = Math.min(bmpEditor.height, Math.ceil((canvas.height - panY) / zoom));

      ctx.beginPath();
      for (let x = startX; x <= endX; x++) {
        ctx.moveTo(x, startY);
        ctx.lineTo(x, endY);
      }
      for (let y = startY; y <= endY; y++) {
        ctx.moveTo(startX, y);
        ctx.lineTo(endX, y);
      }
      ctx.stroke();
    }

    // Draw line preview
    if (lineStart && (activeTool === 'line' || activeTool === 'rectangle')) {
      ctx.strokeStyle = 'rgba(0, 122, 204, 0.8)';
      ctx.lineWidth = 2 / zoom;
      ctx.setLineDash([4 / zoom, 4 / zoom]);
      
      if (activeTool === 'line') {
        ctx.beginPath();
        ctx.moveTo(lineStart.x, lineStart.y);
        ctx.lineTo(lastPos?.x || lineStart.x, lastPos?.y || lineStart.y);
        ctx.stroke();
      } else {
        ctx.strokeRect(
          Math.min(lineStart.x, lastPos?.x || lineStart.x),
          Math.min(lineStart.y, lastPos?.y || lineStart.y),
          Math.abs((lastPos?.x || lineStart.x) - lineStart.x),
          Math.abs((lastPos?.y || lineStart.y) - lineStart.y)
        );
      }
      ctx.setLineDash([]);
    }

    ctx.restore();
  }, [bmpEditor, panX, panY, zoom, showGrid, activeTool, lineStart, lastPos]);

  // Handle resize
  useEffect(() => {
    const container = containerRef.current;
    const canvas = canvasRef.current;
    if (!container || !canvas) return;

    const resizeObserver = new ResizeObserver((entries) => {
      for (const entry of entries) {
        const { width, height } = entry.contentRect;
        canvas.width = width;
        canvas.height = height;
        setViewport(width, height);
        render();
      }
    });

    resizeObserver.observe(container);
    return () => resizeObserver.disconnect();
  }, [setViewport, render]);

  // Initial fit to view
  useEffect(() => {
    if (bmpEditor) {
      setTimeout(fitToView, 100);
    }
  }, [bmpEditor, fitToView]);

  // Re-render on changes
  useEffect(() => {
    render();
  }, [render]);

  // Animation frame for smooth rendering
  useEffect(() => {
    let animationId: number;
    const animate = () => {
      render();
      animationId = requestAnimationFrame(animate);
    };
    animationId = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(animationId);
  }, [render]);

  // Mouse handlers
  const handleMouseDown = useCallback(
    (e: React.MouseEvent) => {
      if (e.button === 1 || (e.button === 0 && e.altKey)) {
        // Middle button or Alt+Left: Pan
        setIsDragging(true);
        setLastPos({ x: e.clientX, y: e.clientY });
        return;
      }

      if (e.button !== 0) return;

      const pos = screenToImage(e.clientX, e.clientY);

      switch (activeTool) {
        case 'select':
          const province = getProvinceAt(pos.x, pos.y);
          selectProvince(province?.id || null);
          break;

        case 'brush':
        case 'pencil':
        case 'eraser':
          if (selectedColor || activeTool === 'eraser') {
            setIsDrawing(true);
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
          setLineStart(pos);
          setLastPos(pos);
          break;
      }
    },
    [
      activeTool,
      selectedColor,
      screenToImage,
      getProvinceAt,
      selectProvince,
      applyBrush,
      applyFill,
      pickColor,
    ]
  );

  const handleMouseMove = useCallback(
    (e: React.MouseEvent) => {
      const pos = screenToImage(e.clientX, e.clientY);

      // Update hovered province
      const province = getProvinceAt(pos.x, pos.y);
      setHoveredProvince(province?.id || null);

      if (isDragging && lastPos) {
        const dx = e.clientX - lastPos.x;
        const dy = e.clientY - lastPos.y;
        setPan(panX + dx, panY + dy);
        setLastPos({ x: e.clientX, y: e.clientY });
        return;
      }

      if (isDrawing && (activeTool === 'brush' || activeTool === 'pencil' || activeTool === 'eraser')) {
        applyBrush(pos.x, pos.y);
      }

      if (lineStart && (activeTool === 'line' || activeTool === 'rectangle')) {
        setLastPos(pos);
      }
    },
    [
      isDragging,
      isDrawing,
      lastPos,
      lineStart,
      activeTool,
      panX,
      panY,
      screenToImage,
      getProvinceAt,
      setHoveredProvince,
      setPan,
      applyBrush,
    ]
  );

  const handleMouseUp = useCallback(
    (e: React.MouseEvent) => {
      if (isDragging) {
        setIsDragging(false);
        setLastPos(null);
        return;
      }

      if (isDrawing) {
        commitChanges();
        setIsDrawing(false);
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
        
        setLineStart(null);
        setLastPos(null);
      }
    },
    [
      isDragging,
      isDrawing,
      lineStart,
      activeTool,
      selectedColor,
      screenToImage,
      commitChanges,
      applyLine,
      applyRect,
    ]
  );

  const handleWheel = useCallback(
    (e: React.WheelEvent) => {
      e.preventDefault();

      const rect = canvasRef.current?.getBoundingClientRect();
      if (!rect) return;

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
    },
    [zoom, panX, panY, setZoom, setPan]
  );

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

  if (!bmpEditor) {
    return (
      <div className="flex-1 flex items-center justify-center bg-ide-bg text-ide-text-muted">
        Loading map...
      </div>
    );
  }

  return (
    <div
      ref={containerRef}
      className="flex-1 overflow-hidden bg-ide-bg"
      style={{ cursor: getCursor() }}
    >
      <canvas
        ref={canvasRef}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={() => {
          setIsDragging(false);
          setIsDrawing(false);
          setHoveredProvince(null);
        }}
        onWheel={handleWheel}
        onContextMenu={(e) => e.preventDefault()}
      />
    </div>
  );
};

export default MapCanvas;
