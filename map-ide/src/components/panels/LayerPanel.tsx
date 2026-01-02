/**
 * Layer Panel Component
 * Controls visibility and settings for map overlay layers
 */

import React from 'react';
import { useMapStore } from '../../stores/mapStore';
import { useProjectStore } from '../../stores/projectStore';
import { LayerType } from '../../types';

interface LayerItemProps {
  label: string;
  icon: string;
  color: string;
  active: boolean;
  count: number;
  onToggle: () => void;
}

const LayerItem: React.FC<LayerItemProps> = ({
  label,
  icon,
  color,
  active,
  count,
  onToggle,
}) => {
  return (
    <div
      className={`flex items-center gap-3 px-3 py-2 rounded cursor-pointer transition-colors ${
        active
          ? 'bg-ide-active text-ide-text'
          : 'hover:bg-ide-hover text-ide-text-muted'
      }`}
      onClick={onToggle}
    >
      <div
        className={`w-4 h-4 rounded border-2 flex items-center justify-center ${
          active ? 'border-blue-500 bg-blue-500' : 'border-gray-500'
        }`}
      >
        {active && (
          <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
            <path
              fillRule="evenodd"
              d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
              clipRule="evenodd"
            />
          </svg>
        )}
      </div>
      <span className="text-lg">{icon}</span>
      <div className="flex-1 min-w-0">
        <div className="font-medium text-sm truncate">{label}</div>
        <div className="text-xs text-ide-text-muted">{count} items</div>
      </div>
      <div
        className="w-3 h-3 rounded-full"
        style={{ backgroundColor: color }}
        title={`${label} border color`}
      />
    </div>
  );
};

const LayerPanel: React.FC = () => {
  const layers = useMapStore((state) => state.layers);
  const showGrid = useMapStore((state) => state.showGrid);
  const showBorders = useMapStore((state) => state.showBorders);
  const toggleLayer = useMapStore((state) => state.toggleLayer);
  const toggleGrid = useMapStore((state) => state.toggleGrid);
  const toggleBorders = useMapStore((state) => state.toggleBorders);

  const provinces = useProjectStore((state) => state.provinces);
  const states = useProjectStore((state) => state.states);
  const strategicRegions = useProjectStore((state) => state.strategicRegions);
  const aiAreas = useProjectStore((state) => state.aiAreas);

  const layerItems: Array<{
    key: LayerType;
    label: string;
    icon: string;
    color: string;
    count: number;
  }> = [
    {
      key: 'provinces',
      label: 'Provinces',
      icon: '🟡',
      color: '#ffcc00',
      count: provinces.size,
    },
    {
      key: 'states',
      label: 'States',
      icon: '🟠',
      color: '#ff8800',
      count: states.size,
    },
    {
      key: 'strategicRegions',
      label: 'Strategic Regions',
      icon: '🔵',
      color: '#00ccff',
      count: strategicRegions.size,
    },
    {
      key: 'aiAreas',
      label: 'AI Areas',
      icon: '🟣',
      color: '#ff00cc',
      count: aiAreas.length,
    },
    {
      key: 'terrain',
      label: 'Terrain',
      icon: '🏔️',
      color: '#88aa44',
      count: 0,
    },
  ];

  return (
    <div className="flex flex-col h-full bg-ide-sidebar">
      {/* Header */}
      <div className="px-4 py-3 border-b border-ide-border">
        <h2 className="text-sm font-semibold text-ide-text uppercase tracking-wider">
          Map Layers
        </h2>
      </div>

      {/* Layer List */}
      <div className="flex-1 overflow-y-auto p-2 space-y-1">
        {layerItems.map((item) => (
          <LayerItem
            key={item.key}
            label={item.label}
            icon={item.icon}
            color={item.color}
            active={layers[item.key]}
            count={item.count}
            onToggle={() => toggleLayer(item.key)}
          />
        ))}
      </div>

      {/* Display Options */}
      <div className="border-t border-ide-border p-3 space-y-2">
        <div className="text-xs font-semibold text-ide-text-muted uppercase mb-2">
          Display Options
        </div>

        {/* Show Borders */}
        <div
          className={`flex items-center gap-3 px-3 py-2 rounded cursor-pointer transition-colors ${
            showBorders
              ? 'bg-ide-active text-ide-text'
              : 'hover:bg-ide-hover text-ide-text-muted'
          }`}
          onClick={toggleBorders}
        >
          <div
            className={`w-4 h-4 rounded border-2 flex items-center justify-center ${
              showBorders ? 'border-green-500 bg-green-500' : 'border-gray-500'
            }`}
          >
            {showBorders && (
              <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fillRule="evenodd"
                  d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                  clipRule="evenodd"
                />
              </svg>
            )}
          </div>
          <span className="text-sm">Show Borders</span>
        </div>

        {/* Show Grid */}
        <div
          className={`flex items-center gap-3 px-3 py-2 rounded cursor-pointer transition-colors ${
            showGrid
              ? 'bg-ide-active text-ide-text'
              : 'hover:bg-ide-hover text-ide-text-muted'
          }`}
          onClick={toggleGrid}
        >
          <div
            className={`w-4 h-4 rounded border-2 flex items-center justify-center ${
              showGrid ? 'border-green-500 bg-green-500' : 'border-gray-500'
            }`}
          >
            {showGrid && (
              <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fillRule="evenodd"
                  d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                  clipRule="evenodd"
                />
              </svg>
            )}
          </div>
          <span className="text-sm">Show Grid (8x+ zoom)</span>
        </div>
      </div>

      {/* Layer Info */}
      <div className="border-t border-ide-border p-3">
        <div className="text-xs text-ide-text-muted">
          <div className="mb-1">
            <strong>Tip:</strong> Enable a layer to show its borders on the map.
          </div>
          <div>
            Hierarchy: Province → State → Region → AI Area
          </div>
        </div>
      </div>
    </div>
  );
};

export default LayerPanel;
