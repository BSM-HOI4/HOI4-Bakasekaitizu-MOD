/**
 * Search Panel
 * 
 * Global search functionality for provinces, states, strategic regions, and AI areas.
 * Supports filtering by type, ID, name, and various properties.
 */

import React, { useState, useMemo, useCallback } from 'react';
import { useProjectStore } from '../../stores/projectStore';
import { useMapStore } from '../../stores/mapStore';
import { Province, State, StrategicRegion, AIArea } from '../../types';
import { rgbToHex } from '../../utils/colorUtils';

type SearchCategory = 'all' | 'provinces' | 'states' | 'regions' | 'aiAreas';

interface SearchResult {
  type: 'province' | 'state' | 'region' | 'aiArea';
  id: number | string;
  name: string;
  details: string;
  data: Province | State | StrategicRegion | AIArea;
}

interface SearchPanelProps {
  onSelectProvince?: (id: number) => void;
  onSelectState?: (id: number) => void;
  onSelectRegion?: (id: number) => void;
  onSelectAIArea?: (name: string) => void;
}

const SearchPanel: React.FC<SearchPanelProps> = ({
  onSelectProvince,
  onSelectState,
  onSelectRegion,
  onSelectAIArea,
}) => {
  const provinces = useProjectStore((state) => state.provinces);
  const states = useProjectStore((state) => state.states);
  const strategicRegions = useProjectStore((state) => state.strategicRegions);
  const aiAreas = useProjectStore((state) => state.aiAreas);
  
  const selectProvince = useMapStore((state) => state.selectProvince);
  const selectState = useMapStore((state) => state.selectState);
  const selectStrategicRegion = useMapStore((state) => state.selectStrategicRegion);

  const [searchQuery, setSearchQuery] = useState('');
  const [category, setCategory] = useState<SearchCategory>('all');
  const [provinceTypeFilter, setProvinceTypeFilter] = useState<'all' | 'land' | 'sea' | 'lake'>('all');

  // Perform search
  const searchResults = useMemo((): SearchResult[] => {
    if (!searchQuery.trim() && category === 'all') return [];
    
    const results: SearchResult[] = [];
    const query = searchQuery.toLowerCase().trim();
    const isIdSearch = /^\d+$/.test(query);
    const searchId = isIdSearch ? parseInt(query) : null;

    // Search provinces
    if (category === 'all' || category === 'provinces') {
      for (const prov of provinces.values()) {
        // Apply type filter
        if (provinceTypeFilter !== 'all' && prov.type !== provinceTypeFilter) {
          continue;
        }

        // Match by ID
        if (searchId !== null && prov.id === searchId) {
          results.push({
            type: 'province',
            id: prov.id,
            name: `Province #${prov.id}`,
            details: `${prov.type} | ${prov.terrain} | ${rgbToHex(prov.color)}`,
            data: prov,
          });
          continue;
        }

        // Match by terrain
        if (query && prov.terrain.toLowerCase().includes(query)) {
          results.push({
            type: 'province',
            id: prov.id,
            name: `Province #${prov.id}`,
            details: `${prov.type} | ${prov.terrain} | ${rgbToHex(prov.color)}`,
            data: prov,
          });
          continue;
        }

        // Match by type
        if (query && prov.type.toLowerCase().includes(query)) {
          results.push({
            type: 'province',
            id: prov.id,
            name: `Province #${prov.id}`,
            details: `${prov.type} | ${prov.terrain} | ${rgbToHex(prov.color)}`,
            data: prov,
          });
        }
      }
    }

    // Search states
    if (category === 'all' || category === 'states') {
      for (const state of states.values()) {
        // Match by ID
        if (searchId !== null && state.id === searchId) {
          results.push({
            type: 'state',
            id: state.id,
            name: `State #${state.id}: ${state.name}`,
            details: `${state.provinces.length} provinces | ${state.stateCategory} | Owner: ${state.owner || 'None'}`,
            data: state,
          });
          continue;
        }

        // Match by name
        if (query && state.name.toLowerCase().includes(query)) {
          results.push({
            type: 'state',
            id: state.id,
            name: `State #${state.id}: ${state.name}`,
            details: `${state.provinces.length} provinces | ${state.stateCategory} | Owner: ${state.owner || 'None'}`,
            data: state,
          });
          continue;
        }

        // Match by owner
        if (query && state.owner && state.owner.toLowerCase().includes(query)) {
          results.push({
            type: 'state',
            id: state.id,
            name: `State #${state.id}: ${state.name}`,
            details: `${state.provinces.length} provinces | ${state.stateCategory} | Owner: ${state.owner}`,
            data: state,
          });
        }
      }
    }

    // Search strategic regions
    if (category === 'all' || category === 'regions') {
      for (const region of strategicRegions.values()) {
        // Match by ID
        if (searchId !== null && region.id === searchId) {
          results.push({
            type: 'region',
            id: region.id,
            name: `Region #${region.id}: ${region.name}`,
            details: `${region.provinces.length} provinces | ${region.weather.length} weather periods`,
            data: region,
          });
          continue;
        }

        // Match by name
        if (query && region.name.toLowerCase().includes(query)) {
          results.push({
            type: 'region',
            id: region.id,
            name: `Region #${region.id}: ${region.name}`,
            details: `${region.provinces.length} provinces | ${region.weather.length} weather periods`,
            data: region,
          });
        }
      }
    }

    // Search AI areas
    if (category === 'all' || category === 'aiAreas') {
      for (const area of aiAreas) {
        // Match by name
        if (!query || area.name.toLowerCase().includes(query)) {
          results.push({
            type: 'aiArea',
            id: area.name,
            name: area.name,
            details: `${area.strategicRegions?.length || 0} regions | ${area.continents?.join(', ') || 'No continents'}`,
            data: area,
          });
        }
      }
    }

    // Sort results
    return results.sort((a, b) => {
      // Sort by type first
      const typeOrder = { province: 0, state: 1, region: 2, aiArea: 3 };
      if (typeOrder[a.type] !== typeOrder[b.type]) {
        return typeOrder[a.type] - typeOrder[b.type];
      }
      // Then by ID
      if (typeof a.id === 'number' && typeof b.id === 'number') {
        return a.id - b.id;
      }
      return String(a.id).localeCompare(String(b.id));
    }).slice(0, 100); // Limit to 100 results
  }, [searchQuery, category, provinceTypeFilter, provinces, states, strategicRegions, aiAreas]);

  // Handle result click
  const handleResultClick = useCallback((result: SearchResult) => {
    switch (result.type) {
      case 'province':
        selectProvince(result.id as number);
        onSelectProvince?.(result.id as number);
        break;
      case 'state':
        selectState(result.id as number);
        onSelectState?.(result.id as number);
        break;
      case 'region':
        selectStrategicRegion(result.id as number);
        onSelectRegion?.(result.id as number);
        break;
      case 'aiArea':
        onSelectAIArea?.(result.id as string);
        break;
    }
  }, [selectProvince, selectState, selectStrategicRegion, onSelectProvince, onSelectState, onSelectRegion, onSelectAIArea]);

  // Get type badge style
  const getTypeBadge = (type: SearchResult['type']) => {
    switch (type) {
      case 'province':
        return 'bg-green-900/50 text-green-400';
      case 'state':
        return 'bg-orange-900/50 text-orange-400';
      case 'region':
        return 'bg-cyan-900/50 text-cyan-400';
      case 'aiArea':
        return 'bg-purple-900/50 text-purple-400';
    }
  };

  return (
    <div className="h-full flex flex-col">
      {/* Search Header */}
      <div className="p-3 border-b border-ide-border space-y-2">
        <h3 className="text-sm font-semibold text-ide-text">Search</h3>
        
        {/* Search Input */}
        <input
          type="text"
          placeholder="Search by ID, name, terrain..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full px-3 py-2 bg-ide-bg border border-ide-border rounded text-ide-text text-sm"
        />

        {/* Category Filter */}
        <div className="flex flex-wrap gap-1">
          {[
            { value: 'all', label: 'All' },
            { value: 'provinces', label: 'Provinces' },
            { value: 'states', label: 'States' },
            { value: 'regions', label: 'Regions' },
            { value: 'aiAreas', label: 'AI Areas' },
          ].map(({ value, label }) => (
            <button
              key={value}
              onClick={() => setCategory(value as SearchCategory)}
              className={`px-2 py-1 rounded text-xs ${
                category === value
                  ? 'bg-blue-600 text-white'
                  : 'bg-ide-hover text-ide-text hover:bg-ide-active'
              }`}
            >
              {label}
            </button>
          ))}
        </div>

        {/* Province Type Filter */}
        {(category === 'all' || category === 'provinces') && (
          <div className="flex gap-1">
            <span className="text-xs text-ide-text-muted py-1">Province type:</span>
            {['all', 'land', 'sea', 'lake'].map((type) => (
              <button
                key={type}
                onClick={() => setProvinceTypeFilter(type as typeof provinceTypeFilter)}
                className={`px-2 py-0.5 rounded text-xs ${
                  provinceTypeFilter === type
                    ? 'bg-green-600 text-white'
                    : 'bg-ide-hover text-ide-text hover:bg-ide-active'
                }`}
              >
                {type}
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Results */}
      <div className="flex-1 overflow-y-auto">
        {searchQuery.trim() === '' && category === 'all' ? (
          <div className="p-4 text-center text-ide-text-muted text-sm">
            Enter a search query or select a category
          </div>
        ) : searchResults.length === 0 ? (
          <div className="p-4 text-center text-ide-text-muted text-sm">
            No results found
          </div>
        ) : (
          <div className="divide-y divide-ide-border/50">
            {searchResults.map((result, idx) => (
              <button
                key={`${result.type}-${result.id}-${idx}`}
                onClick={() => handleResultClick(result)}
                className="w-full px-3 py-2 text-left hover:bg-ide-hover transition-colors"
              >
                <div className="flex items-start gap-2">
                  <span className={`text-xs px-1.5 py-0.5 rounded ${getTypeBadge(result.type)}`}>
                    {result.type === 'aiArea' ? 'AI' : result.type.charAt(0).toUpperCase()}
                  </span>
                  <div className="flex-1 min-w-0">
                    <div className="text-sm text-ide-text truncate">
                      {result.name}
                    </div>
                    <div className="text-xs text-ide-text-muted truncate">
                      {result.details}
                    </div>
                  </div>
                </div>
              </button>
            ))}
            {searchResults.length === 100 && (
              <div className="px-3 py-2 text-center text-xs text-ide-text-muted">
                Showing first 100 results
              </div>
            )}
          </div>
        )}
      </div>

      {/* Stats Footer */}
      <div className="p-2 border-t border-ide-border">
        <div className="text-xs text-ide-text-muted">
          {searchResults.length} results
          {searchQuery && ` for "${searchQuery}"`}
        </div>
      </div>
    </div>
  );
};

export default SearchPanel;
