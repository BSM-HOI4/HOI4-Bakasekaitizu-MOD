import React, { useState, useMemo } from 'react';
import { useProjectStore } from '../../stores/projectStore';
import { useMapStore } from '../../stores/mapStore';
import { Province, RGB } from '../../types';
import { rgbToHex } from '../../utils/colorUtils';

const ColorPalette: React.FC = () => {
  const provinces = useProjectStore((state) => state.provinces);
  const selectedColor = useMapStore((state) => state.selectedColor);
  const setSelectedColor = useMapStore((state) => state.setSelectedColor);
  const selectProvince = useMapStore((state) => state.selectProvince);

  const [filter, setFilter] = useState<'all' | 'land' | 'sea' | 'lake'>('all');
  const [search, setSearch] = useState('');

  const filteredProvinces = useMemo(() => {
    let result = provinces;

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

  const isColorSelected = (color: RGB): boolean => {
    if (!selectedColor) return false;
    return (
      selectedColor.r === color.r &&
      selectedColor.g === color.g &&
      selectedColor.b === color.b
    );
  };

  return (
    <div className="p-2 flex flex-col h-full">
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
                  ? 'border-ide-highlight'
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

      {/* Selected Color Info */}
      {selectedColor && (
        <div className="mt-2 p-2 bg-ide-panel rounded">
          <div className="flex items-center gap-2">
            <div
              className="w-8 h-8 rounded border border-ide-border"
              style={{
                backgroundColor: rgbToHex(selectedColor),
              }}
            />
            <div className="text-xs">
              <div className="text-ide-text">
                RGB({selectedColor.r}, {selectedColor.g}, {selectedColor.b})
              </div>
              <div className="text-ide-text-muted">
                {rgbToHex(selectedColor)}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ColorPalette;
