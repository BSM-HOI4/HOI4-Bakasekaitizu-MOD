import React from 'react';
import { useMapStore } from '../../stores/mapStore';
import { ToolType } from '../../types';

const tools: { type: ToolType; icon: string; label: string; shortcut: string }[] = [
  { type: 'select', icon: '👆', label: 'Select', shortcut: 'V' },
  { type: 'brush', icon: '🖌️', label: 'Brush', shortcut: 'B' },
  { type: 'fill', icon: '🪣', label: 'Fill', shortcut: 'G' },
  { type: 'pencil', icon: '✏️', label: 'Pencil', shortcut: 'P' },
  { type: 'eyedropper', icon: '🔍', label: 'Eyedropper', shortcut: 'I' },
  { type: 'eraser', icon: '🧹', label: 'Eraser', shortcut: 'E' },
  { type: 'line', icon: '📐', label: 'Line', shortcut: 'L' },
  { type: 'rectangle', icon: '🔲', label: 'Rectangle', shortcut: 'R' },
];

const ToolBar: React.FC = () => {
  const activeTool = useMapStore((state) => state.activeTool);
  const setActiveTool = useMapStore((state) => state.setActiveTool);
  const brushSize = useMapStore((state) => state.brushSize);
  const setBrushSize = useMapStore((state) => state.setBrushSize);
  const brushShape = useMapStore((state) => state.brushShape);
  const setBrushShape = useMapStore((state) => state.setBrushShape);
  const selectedColor = useMapStore((state) => state.selectedColor);
  const zoomIn = useMapStore((state) => state.zoomIn);
  const zoomOut = useMapStore((state) => state.zoomOut);
  const fitToView = useMapStore((state) => state.fitToView);
  const zoom = useMapStore((state) => state.zoom);

  return (
    <div className="flex items-center gap-1">
      {/* Tools */}
      {tools.map((tool) => (
        <button
          key={tool.type}
          onClick={() => setActiveTool(tool.type)}
          className={`p-2 rounded ${
            activeTool === tool.type
              ? 'bg-ide-accent text-white'
              : 'hover:bg-ide-panel text-ide-text'
          }`}
          title={`${tool.label} (${tool.shortcut})`}
        >
          {tool.icon}
        </button>
      ))}

      <div className="w-px h-6 bg-ide-border mx-1" />

      {/* Brush settings */}
      {(activeTool === 'brush' || activeTool === 'eraser') && (
        <>
          <div className="flex items-center gap-2 mx-2">
            <span className="text-ide-text-muted text-xs">Size:</span>
            <input
              type="range"
              min="1"
              max="50"
              value={brushSize}
              onChange={(e) => setBrushSize(parseInt(e.target.value))}
              className="w-24 accent-ide-accent"
            />
            <span className="text-ide-text text-xs w-6">{brushSize}</span>
          </div>

          <div className="flex items-center gap-1 mx-2">
            <button
              onClick={() => setBrushShape('circle')}
              className={`px-2 py-1 rounded text-xs ${
                brushShape === 'circle'
                  ? 'bg-ide-accent text-white'
                  : 'bg-ide-panel text-ide-text'
              }`}
            >
              ●
            </button>
            <button
              onClick={() => setBrushShape('square')}
              className={`px-2 py-1 rounded text-xs ${
                brushShape === 'square'
                  ? 'bg-ide-accent text-white'
                  : 'bg-ide-panel text-ide-text'
              }`}
            >
              ■
            </button>
          </div>

          <div className="w-px h-6 bg-ide-border mx-1" />
        </>
      )}

      {/* Selected Color */}
      {selectedColor && (
        <div className="flex items-center gap-2 mx-2">
          <span className="text-ide-text-muted text-xs">Color:</span>
          <div
            className="w-6 h-6 border border-ide-border rounded"
            style={{
              backgroundColor: `rgb(${selectedColor.r}, ${selectedColor.g}, ${selectedColor.b})`,
            }}
            title={`RGB(${selectedColor.r}, ${selectedColor.g}, ${selectedColor.b})`}
          />
        </div>
      )}

      <div className="flex-1" />

      {/* Zoom controls */}
      <div className="flex items-center gap-1">
        <button
          onClick={zoomOut}
          className="p-1 hover:bg-ide-panel text-ide-text rounded"
          title="Zoom Out (-)"
        >
          ➖
        </button>
        <span className="text-ide-text text-xs w-12 text-center">
          {Math.round(zoom * 100)}%
        </span>
        <button
          onClick={zoomIn}
          className="p-1 hover:bg-ide-panel text-ide-text rounded"
          title="Zoom In (+)"
        >
          ➕
        </button>
        <button
          onClick={fitToView}
          className="p-1 hover:bg-ide-panel text-ide-text rounded ml-1"
          title="Fit to View"
        >
          🔳
        </button>
      </div>
    </div>
  );
};

export default ToolBar;
