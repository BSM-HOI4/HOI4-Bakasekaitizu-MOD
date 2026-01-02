/**
 * RGB Color Circle Component
 * 
 * A color picker that displays available colors in a circular HSV wheel.
 * Colors already in use (existing province colors) are marked as unavailable
 * and cannot be selected.
 */

import React, { useRef, useEffect, useState, useCallback, useMemo } from 'react';
import { RGB } from '../../types';
import { hsvToRgb, rgbToHsv, rgbToKey, rgbToHex } from '../../utils/colorUtils';

interface ColorCircleProps {
  /** Currently selected color */
  selectedColor: RGB | null;
  /** Set of used color keys (format: "r,g,b") that should be marked unavailable */
  usedColors: Set<string>;
  /** Callback when a color is selected */
  onColorSelect: (color: RGB) => void;
  /** Size of the color circle in pixels */
  size?: number;
}

const ColorCircle: React.FC<ColorCircleProps> = ({
  selectedColor,
  usedColors,
  onColorSelect,
  size = 200,
}) => {
  const wheelCanvasRef = useRef<HTMLCanvasElement>(null);
  const brightnessCanvasRef = useRef<HTMLCanvasElement>(null);
  const [currentHue, setCurrentHue] = useState(0);
  const [currentSat, setCurrentSat] = useState(1);
  const [currentVal, setCurrentVal] = useState(1);
  const [isDraggingWheel, setIsDraggingWheel] = useState(false);
  const [isDraggingBrightness, setIsDraggingBrightness] = useState(false);
  const [hoveredColor, setHoveredColor] = useState<RGB | null>(null);

  const wheelRadius = size / 2 - 10;
  const wheelCenter = size / 2;
  const brightnessBarWidth = 20;
  const brightnessBarHeight = size - 40;

  // Check if a color is available (not used)
  const isColorAvailable = useCallback((color: RGB): boolean => {
    const key = rgbToKey(color);
    return !usedColors.has(key);
  }, [usedColors]);

  // Get the current RGB color from HSV
  const currentRgb = useMemo(() => {
    return hsvToRgb({ h: currentHue, s: currentSat, v: currentVal });
  }, [currentHue, currentSat, currentVal]);

  // Check if current color is available
  const isCurrentColorAvailable = useMemo(() => {
    return isColorAvailable(currentRgb);
  }, [currentRgb, isColorAvailable]);

  // Update HSV from selected color
  useEffect(() => {
    if (selectedColor) {
      const hsv = rgbToHsv(selectedColor);
      setCurrentHue(hsv.h);
      setCurrentSat(hsv.s);
      setCurrentVal(hsv.v);
    }
  }, [selectedColor]);

  // Draw the color wheel
  const drawColorWheel = useCallback(() => {
    const canvas = wheelCanvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d')!;
    const imageData = ctx.createImageData(size, size);
    const data = imageData.data;

    for (let y = 0; y < size; y++) {
      for (let x = 0; x < size; x++) {
        const dx = x - wheelCenter;
        const dy = y - wheelCenter;
        const distance = Math.sqrt(dx * dx + dy * dy);

        const idx = (y * size + x) * 4;

        if (distance <= wheelRadius) {
          // Calculate hue from angle
          let angle = Math.atan2(dy, dx);
          if (angle < 0) angle += Math.PI * 2;
          const hue = angle / (Math.PI * 2);

          // Saturation from distance
          const saturation = distance / wheelRadius;

          // Convert to RGB
          const rgb = hsvToRgb({ h: hue, s: saturation, v: currentVal });

          // Check if this color is used
          const isUsed = usedColors.has(rgbToKey(rgb));

          if (isUsed) {
            // Draw used colors as darker/grayed out with pattern
            data[idx] = Math.floor(rgb.r * 0.3);
            data[idx + 1] = Math.floor(rgb.g * 0.3);
            data[idx + 2] = Math.floor(rgb.b * 0.3);
            data[idx + 3] = 255;

            // Add diagonal stripe pattern for used colors
            if ((x + y) % 4 < 2) {
              data[idx] = Math.min(255, data[idx] + 30);
              data[idx + 1] = Math.min(255, data[idx + 1] + 30);
              data[idx + 2] = Math.min(255, data[idx + 2] + 30);
            }
          } else {
            // Available color - full brightness
            data[idx] = rgb.r;
            data[idx + 1] = rgb.g;
            data[idx + 2] = rgb.b;
            data[idx + 3] = 255;
          }
        } else if (distance <= wheelRadius + 2) {
          // Border
          data[idx] = 60;
          data[idx + 1] = 60;
          data[idx + 2] = 60;
          data[idx + 3] = 255;
        } else {
          // Transparent
          data[idx + 3] = 0;
        }
      }
    }

    ctx.putImageData(imageData, 0, 0);

    // Draw selection indicator
    const selAngle = currentHue * Math.PI * 2;
    const selDist = currentSat * wheelRadius;
    const selX = wheelCenter + Math.cos(selAngle) * selDist;
    const selY = wheelCenter + Math.sin(selAngle) * selDist;

    ctx.beginPath();
    ctx.arc(selX, selY, 8, 0, Math.PI * 2);
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 2;
    ctx.stroke();
    ctx.beginPath();
    ctx.arc(selX, selY, 6, 0, Math.PI * 2);
    ctx.strokeStyle = '#000000';
    ctx.lineWidth = 1;
    ctx.stroke();
  }, [size, wheelCenter, wheelRadius, currentVal, currentHue, currentSat, usedColors]);

  // Draw brightness bar
  const drawBrightnessBar = useCallback(() => {
    const canvas = brightnessCanvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d')!;
    const imageData = ctx.createImageData(brightnessBarWidth, brightnessBarHeight);
    const data = imageData.data;

    for (let y = 0; y < brightnessBarHeight; y++) {
      const value = 1 - y / brightnessBarHeight;
      const rgb = hsvToRgb({ h: currentHue, s: currentSat, v: value });

      for (let x = 0; x < brightnessBarWidth; x++) {
        const idx = (y * brightnessBarWidth + x) * 4;
        data[idx] = rgb.r;
        data[idx + 1] = rgb.g;
        data[idx + 2] = rgb.b;
        data[idx + 3] = 255;
      }
    }

    ctx.putImageData(imageData, 0, 0);

    // Draw selection indicator
    const selY = (1 - currentVal) * brightnessBarHeight;
    ctx.fillStyle = '#ffffff';
    ctx.beginPath();
    ctx.moveTo(0, selY);
    ctx.lineTo(5, selY - 5);
    ctx.lineTo(5, selY + 5);
    ctx.closePath();
    ctx.fill();
    ctx.beginPath();
    ctx.moveTo(brightnessBarWidth, selY);
    ctx.lineTo(brightnessBarWidth - 5, selY - 5);
    ctx.lineTo(brightnessBarWidth - 5, selY + 5);
    ctx.closePath();
    ctx.fill();
  }, [brightnessBarWidth, brightnessBarHeight, currentHue, currentSat, currentVal]);

  // Redraw on changes
  useEffect(() => {
    drawColorWheel();
  }, [drawColorWheel]);

  useEffect(() => {
    drawBrightnessBar();
  }, [drawBrightnessBar]);

  // Handle wheel mouse events
  const handleWheelMouseDown = useCallback((e: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = wheelCanvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const dx = x - wheelCenter;
    const dy = y - wheelCenter;
    const distance = Math.sqrt(dx * dx + dy * dy);

    if (distance <= wheelRadius) {
      setIsDraggingWheel(true);
      updateWheelPosition(x, y);
    }
  }, [wheelCenter, wheelRadius]);

  const updateWheelPosition = useCallback((x: number, y: number) => {
    const dx = x - wheelCenter;
    const dy = y - wheelCenter;
    let distance = Math.sqrt(dx * dx + dy * dy);
    distance = Math.min(distance, wheelRadius);

    let angle = Math.atan2(dy, dx);
    if (angle < 0) angle += Math.PI * 2;

    const hue = angle / (Math.PI * 2);
    const saturation = distance / wheelRadius;

    setCurrentHue(hue);
    setCurrentSat(saturation);
  }, [wheelCenter, wheelRadius]);

  const handleWheelMouseMove = useCallback((e: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = wheelCanvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    // Update hovered color
    const dx = x - wheelCenter;
    const dy = y - wheelCenter;
    const distance = Math.sqrt(dx * dx + dy * dy);

    if (distance <= wheelRadius) {
      let angle = Math.atan2(dy, dx);
      if (angle < 0) angle += Math.PI * 2;
      const hue = angle / (Math.PI * 2);
      const saturation = distance / wheelRadius;
      setHoveredColor(hsvToRgb({ h: hue, s: saturation, v: currentVal }));
    } else {
      setHoveredColor(null);
    }

    if (isDraggingWheel) {
      updateWheelPosition(x, y);
    }
  }, [isDraggingWheel, updateWheelPosition, wheelCenter, wheelRadius, currentVal]);

  // Handle brightness bar mouse events
  const handleBrightnessMouseDown = useCallback((e: React.MouseEvent<HTMLCanvasElement>) => {
    setIsDraggingBrightness(true);
    updateBrightnessPosition(e);
  }, []);

  const updateBrightnessPosition = useCallback((e: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = brightnessCanvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    const y = e.clientY - rect.top;
    const value = 1 - Math.max(0, Math.min(1, y / brightnessBarHeight));
    setCurrentVal(value);
  }, [brightnessBarHeight]);

  const handleBrightnessMouseMove = useCallback((e: React.MouseEvent<HTMLCanvasElement>) => {
    if (isDraggingBrightness) {
      updateBrightnessPosition(e);
    }
  }, [isDraggingBrightness, updateBrightnessPosition]);

  // Handle mouse up
  useEffect(() => {
    const handleMouseUp = () => {
      setIsDraggingWheel(false);
      setIsDraggingBrightness(false);
    };

    window.addEventListener('mouseup', handleMouseUp);
    return () => window.removeEventListener('mouseup', handleMouseUp);
  }, []);

  // Handle color selection
  const handleSelectColor = useCallback(() => {
    if (isCurrentColorAvailable) {
      onColorSelect(currentRgb);
    }
  }, [currentRgb, isCurrentColorAvailable, onColorSelect]);

  // Find nearest available color
  const findNearestAvailable = useCallback((): RGB | null => {
    if (isCurrentColorAvailable) return currentRgb;

    // Search nearby colors
    for (let dh = 0; dh < 1; dh += 0.01) {
      for (let ds = 0; ds <= 1; ds += 0.05) {
        for (let dv = 0; dv <= 1; dv += 0.05) {
          const variations = [
            { h: (currentHue + dh) % 1, s: Math.min(1, currentSat + ds), v: Math.min(1, currentVal + dv) },
            { h: (currentHue + dh) % 1, s: Math.max(0, currentSat - ds), v: Math.min(1, currentVal + dv) },
            { h: (currentHue - dh + 1) % 1, s: Math.min(1, currentSat + ds), v: Math.max(0, currentVal - dv) },
            { h: (currentHue - dh + 1) % 1, s: Math.max(0, currentSat - ds), v: Math.max(0, currentVal - dv) },
          ];

          for (const hsv of variations) {
            const rgb = hsvToRgb(hsv);
            if (isColorAvailable(rgb)) {
              return rgb;
            }
          }
        }
      }
    }
    return null;
  }, [currentHue, currentSat, currentVal, currentRgb, isColorAvailable, isCurrentColorAvailable]);

  const handleFindAvailable = useCallback(() => {
    const available = findNearestAvailable();
    if (available) {
      const hsv = rgbToHsv(available);
      setCurrentHue(hsv.h);
      setCurrentSat(hsv.s);
      setCurrentVal(hsv.v);
    }
  }, [findNearestAvailable]);

  // Calculate statistics
  const stats = useMemo(() => {
    const total = 256 * 256 * 256;
    const used = usedColors.size;
    const available = total - used;
    return { total, used, available };
  }, [usedColors]);

  return (
    <div className="flex flex-col gap-3 p-3 bg-ide-panel rounded-lg">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-medium text-ide-text">Color Picker</h3>
        <div className="text-xs text-ide-text-muted">
          {stats.used.toLocaleString()} used / {stats.available.toLocaleString()} available
        </div>
      </div>

      {/* Color wheel and brightness bar */}
      <div className="flex gap-3 items-center justify-center">
        {/* Color wheel */}
        <canvas
          ref={wheelCanvasRef}
          width={size}
          height={size}
          className="cursor-crosshair"
          onMouseDown={handleWheelMouseDown}
          onMouseMove={handleWheelMouseMove}
          onMouseLeave={() => setHoveredColor(null)}
        />

        {/* Brightness bar */}
        <canvas
          ref={brightnessCanvasRef}
          width={brightnessBarWidth}
          height={brightnessBarHeight}
          className="cursor-ns-resize rounded"
          style={{ border: '1px solid #444' }}
          onMouseDown={handleBrightnessMouseDown}
          onMouseMove={handleBrightnessMouseMove}
        />
      </div>

      {/* Current color preview */}
      <div className="flex gap-3 items-center">
        <div className="flex flex-col gap-1 flex-1">
          <div className="text-xs text-ide-text-muted">Selected Color</div>
          <div className="flex items-center gap-2">
            <div
              className="w-10 h-10 rounded border-2"
              style={{
                backgroundColor: rgbToHex(currentRgb),
                borderColor: isCurrentColorAvailable ? '#4ade80' : '#ef4444',
              }}
            />
            <div className="flex flex-col">
              <span className="text-xs font-mono text-ide-text">
                RGB({currentRgb.r}, {currentRgb.g}, {currentRgb.b})
              </span>
              <span className="text-xs font-mono text-ide-text-muted">
                {rgbToHex(currentRgb)}
              </span>
              <span className={`text-xs ${isCurrentColorAvailable ? 'text-green-500' : 'text-red-500'}`}>
                {isCurrentColorAvailable ? '✓ Available' : '✗ Already used'}
              </span>
            </div>
          </div>
        </div>

        {/* Hovered color info */}
        {hoveredColor && (
          <div className="flex flex-col gap-1">
            <div className="text-xs text-ide-text-muted">Hover</div>
            <div className="flex items-center gap-2">
              <div
                className="w-6 h-6 rounded border"
                style={{
                  backgroundColor: rgbToHex(hoveredColor),
                  borderColor: isColorAvailable(hoveredColor) ? '#4ade80' : '#ef4444',
                }}
              />
              <span className={`text-xs ${isColorAvailable(hoveredColor) ? 'text-green-500' : 'text-red-500'}`}>
                {isColorAvailable(hoveredColor) ? '✓' : '✗'}
              </span>
            </div>
          </div>
        )}
      </div>

      {/* RGB inputs */}
      <div className="grid grid-cols-3 gap-2">
        <div className="flex flex-col gap-1">
          <label className="text-xs text-ide-text-muted">R</label>
          <input
            type="number"
            min="0"
            max="255"
            value={currentRgb.r}
            onChange={(e) => {
              const r = Math.max(0, Math.min(255, parseInt(e.target.value) || 0));
              const hsv = rgbToHsv({ r, g: currentRgb.g, b: currentRgb.b });
              setCurrentHue(hsv.h);
              setCurrentSat(hsv.s);
              setCurrentVal(hsv.v);
            }}
            className="w-full px-2 py-1 bg-ide-bg border border-ide-border rounded text-ide-text text-xs text-center"
          />
        </div>
        <div className="flex flex-col gap-1">
          <label className="text-xs text-ide-text-muted">G</label>
          <input
            type="number"
            min="0"
            max="255"
            value={currentRgb.g}
            onChange={(e) => {
              const g = Math.max(0, Math.min(255, parseInt(e.target.value) || 0));
              const hsv = rgbToHsv({ r: currentRgb.r, g, b: currentRgb.b });
              setCurrentHue(hsv.h);
              setCurrentSat(hsv.s);
              setCurrentVal(hsv.v);
            }}
            className="w-full px-2 py-1 bg-ide-bg border border-ide-border rounded text-ide-text text-xs text-center"
          />
        </div>
        <div className="flex flex-col gap-1">
          <label className="text-xs text-ide-text-muted">B</label>
          <input
            type="number"
            min="0"
            max="255"
            value={currentRgb.b}
            onChange={(e) => {
              const b = Math.max(0, Math.min(255, parseInt(e.target.value) || 0));
              const hsv = rgbToHsv({ r: currentRgb.r, g: currentRgb.g, b });
              setCurrentHue(hsv.h);
              setCurrentSat(hsv.s);
              setCurrentVal(hsv.v);
            }}
            className="w-full px-2 py-1 bg-ide-bg border border-ide-border rounded text-ide-text text-xs text-center"
          />
        </div>
      </div>

      {/* Action buttons */}
      <div className="flex gap-2">
        <button
          onClick={handleSelectColor}
          disabled={!isCurrentColorAvailable}
          className={`flex-1 px-3 py-2 rounded text-sm font-medium transition-colors ${
            isCurrentColorAvailable
              ? 'bg-blue-600 hover:bg-blue-700 text-white'
              : 'bg-gray-600 text-gray-400 cursor-not-allowed'
          }`}
        >
          {isCurrentColorAvailable ? 'Use This Color' : 'Color Unavailable'}
        </button>
        {!isCurrentColorAvailable && (
          <button
            onClick={handleFindAvailable}
            className="px-3 py-2 bg-ide-hover hover:bg-ide-active rounded text-sm text-ide-text transition-colors"
            title="Find nearest available color"
          >
            Find Similar
          </button>
        )}
      </div>

      {/* Legend */}
      <div className="flex items-center gap-4 text-xs text-ide-text-muted border-t border-ide-border pt-2">
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 rounded bg-gradient-to-r from-red-500 to-blue-500" />
          <span>Available</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 rounded bg-gray-600" style={{ 
            background: 'repeating-linear-gradient(45deg, #333, #333 2px, #444 2px, #444 4px)' 
          }} />
          <span>Used (unavailable)</span>
        </div>
      </div>
    </div>
  );
};

export default ColorCircle;
