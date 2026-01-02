import React, { useState, useMemo } from 'react';
import { useProjectStore } from '../../stores/projectStore';
import { useMapStore } from '../../stores/mapStore';
import { Province, RGB } from '../../types';
import { rgbToHex, rgbToKey } from '../../utils/colorUtils';
import ColorCircle from './ColorCircle';

type ViewMode = 'grid' | 'picker';

const ColorPalette: React.FC = () => {
  const provinces = useProjectStore((state) => state.provinces);
  const provinceByColor = useProjectStore((state) => state.provinceByColor);
  const selectedColor = useMapStore((state) => state.selectedColor);
  const setSelectedColor = useMapStore((state) => state.setSelectedColor);
  const selectProvince = useMapStore((state) => state.selectProvince);

  const [viewMode, setViewMode] = useState<ViewMode>('picker');
  const [filter, setFilter] = useState<'all' | 'land' | 'sea' | 'lake'>('all');
  const [search, setSearch] = useState('');

  // Get all used colors as a Set for the color picker
  const usedColors = useMemo(() => {
    const colors = new Set<string>();
    for (const province of provinces.values()) {
      colors.add(rgbToKey(province.color));
    }
    return colors;
  }, [provinces]);

  const filteredProvinces = useMemo(() => {
    let result = Array.from(provinces.values());

    // Filter by type
    if (filter !== 'all') {
      result = result.filter((p) => p.type === filter);
    }

    // Filter by search
    if (search) {
      const searchLower = search.toLowerCase();
      result = result.filter(
        (p) =>
          p.id.toString().includes(searchLower) ||
          p.terrain.toLowerCase().includes(searchLower)
      );
    }

    // Sort by ID
    return result.sort((a, b) => a.id - b.id);
  }, [provinces, filter, search]);

  const handleColorClick = (province: Province) => {
    setSelectedColor(province.color);
    selectProvince(province.id);
  };

  const handleNewColorSelect = (color: RGB) => {
    setSelectedColor(color);
    // Clear province selection since this is a new color
    selectProvince(null);
  };

  const isColorSelected = (color: RGB): boolean => {
    if (!selectedColor) return false;
    return (
      selectedColor.r === color.r &&
      selectedColor.g === color.g &&
      selectedColor.b === color.b
    );
  };

  // Find province for selected color
  const selectedProvince = useMemo(() => {
    if (!selectedColor) return null;
    return provinceByColor.get(rgbToKey(selectedColor)) || null;
  }, [selectedColor, provinceByColor]);

  return (
    <div className="p-2 flex flex-col h-full">
      {/* View Mode Toggle */}
      <div className="flex gap-1 mb-3 bg-ide-bg rounded p-1">
        <button
          onClick={() => setViewMode('picker')}
          className={`flex-1 px-3 py-1.5 text-xs rounded transition-colors ${
            viewMode === 'picker'
              ? 'bg-ide-accent text-white'
              : 'text-ide-text-muted hover:bg-ide-hover'
          }`}
        >
          🎨 Color Picker
        </button>
        <button
          onClick={() => setViewMode('grid')}
          className={`flex-1 px-3 py-1.5 text-xs rounded transition-colors ${
            viewMode === 'grid'
              ? 'bg-ide-accent text-white'
              : 'text-ide-text-muted hover:bg-ide-hover'
          }`}
        >
          📋 Province Colors
        </button>
      </div>

      {viewMode === 'picker' ? (
        /* Color Circle Picker */
        <div className="flex-1 overflow-auto">
          <ColorCircle
            selectedColor={selectedColor}
            usedColors={usedColors}
            onColorSelect={handleNewColorSelect}
            size={220}
          />
          
          {/* Info about new color usage */}
          <div className="mt-3 p-2 bg-ide-bg rounded text-xs text-ide-text-muted">
            <div className="font-medium text-ide-text mb-1">💡 New Province Color</div>
            <p>
              Use the color picker to select a unique color for a new province.
              Colors already assigned to existing provinces are shown as unavailable.
            </p>
          </div>
        </div>
      ) : (
        /* Grid View */
        <div className="flex flex-col flex-1 overflow-hidden">
          {/* Search */}
          <input
            type="text"
            placeholder="Search by ID or terrain..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full px-2 py-1 mb-2 bg-ide-panel border border-ide-border rounded text-ide-text text-xs focus:outline-none focus:border-ide-accent"
          />

          {/* Filter */}
          <div className="flex gap-1 mb-2">
            {(['all', 'land', 'sea', 'lake'] as const).map((f) => (
              <button
                key={f}
                onClick={() => setFilter(f)}
                className={`px-2 py-1 text-xs rounded ${
                  filter === f
                    ? 'bg-ide-accent text-white'
                    : 'bg-ide-panel text-ide-text hover:bg-ide-border'
                }`}
              >
                {f}
              </button>
            ))}
          </div>

          {/* Count */}
          <div className="text-ide-text-muted text-xs mb-2">
            {filteredProvinces.length} provinces
          </div>

          {/* Color Grid */}
          <div className="flex-1 overflow-auto">
            <div className="grid grid-cols-6 gap-1">
              {filteredProvinces.slice(0, 500).map((province) => (
                <button
                  key={province.id}
                  onClick={() => handleColorClick(province)}
                  className={`aspect-square rounded border-2 ${
                    isColorSelected(province.color)
                      ? 'border-ide-highlight ring-2 ring-ide-accent'
                      : 'border-transparent hover:border-ide-accent'
                  }`}
                  style={{
                    backgroundColor: rgbToHex(province.color),
                  }}
                  title={`ID: ${province.id}\nType: ${province.type}\nTerrain: ${province.terrain}\nRGB: (${province.color.r}, ${province.color.g}, ${province.color.b})`}
                />
              ))}
            </div>
            
            {filteredProvinces.length > 500 && (
              <div className="text-ide-text-muted text-xs text-center mt-2">
                Showing first 500 of {filteredProvinces.length}
              </div>
            )}
          </div>
        </div>
      )}

      {/* Selected Color Info */}
      {selectedColor && (
        <div className="mt-2 p-2 bg-ide-panel rounded border border-ide-border">
          <div className="flex items-center gap-3">
            <div
              className="w-10 h-10 rounded border-2 border-ide-border shadow-inner"
              style={{
                backgroundColor: rgbToHex(selectedColor),
              }}
            />
            <div className="flex-1 min-w-0">
              <div className="text-xs font-medium text-ide-text">
                {selectedProvince ? `Province #${selectedProvince.id}` : 'New Color'}
              </div>
              <div className="text-xs text-ide-text-muted font-mono">
                RGB({selectedColor.r}, {selectedColor.g}, {selectedColor.b})
              </div>
              <div className="text-xs text-ide-text-muted font-mono">
                {rgbToHex(selectedColor)}
              </div>
              {selectedProvince && (
                <div className="text-xs text-ide-text-muted">
                  {selectedProvince.type} • {selectedProvince.terrain}
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ColorPalette;
