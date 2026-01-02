import React from 'react';
import { useMapStore } from '../../stores/mapStore';
import { useProjectStore } from '../../stores/projectStore';
import { rgbToHex } from '../../utils/colorUtils';

const PropertyPanel: React.FC = () => {
  const selectedProvinceId = useMapStore((state) => state.selectedProvinceId);
  const provinceById = useProjectStore((state) => state.provinceById);
  const stateById = useProjectStore((state) => state.stateById);
  const strategicRegionById = useProjectStore((state) => state.strategicRegionById);

  const province = selectedProvinceId
    ? provinceById.get(selectedProvinceId)
    : null;
  const state = province?.stateId ? stateById.get(province.stateId) : null;
  const region = province?.strategicRegionId
    ? strategicRegionById.get(province.strategicRegionId)
    : null;

  return (
    <div className="w-72 bg-ide-sidebar border-l border-ide-border flex flex-col overflow-hidden">
      <div className="p-2 border-b border-ide-border">
        <h2 className="text-ide-text text-sm font-medium">Properties</h2>
      </div>

      <div className="flex-1 overflow-auto p-2 space-y-3">
        {!province ? (
          <div className="text-ide-text-muted text-xs text-center py-8">
            Select a province to view properties
          </div>
        ) : (
          <>
            {/* Province Info */}
            <div className="bg-ide-panel p-3 rounded">
              <h3 className="text-ide-text text-xs font-medium mb-2 flex items-center gap-2">
                <span>📍</span> Province
              </h3>
              <div className="space-y-2 text-xs">
                <div className="flex justify-between">
                  <span className="text-ide-text-muted">ID</span>
                  <span className="text-ide-text">{province.id}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-ide-text-muted">Color</span>
                  <div className="flex items-center gap-2">
                    <div
                      className="w-4 h-4 rounded border border-ide-border"
                      style={{ backgroundColor: rgbToHex(province.color) }}
                    />
                    <span className="text-ide-text font-mono text-xs">
                      {rgbToHex(province.color)}
                    </span>
                  </div>
                </div>
                <div className="flex justify-between">
                  <span className="text-ide-text-muted">Type</span>
                  <span className="text-ide-text capitalize">{province.type}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-ide-text-muted">Terrain</span>
                  <span className="text-ide-text capitalize">{province.terrain}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-ide-text-muted">Coastal</span>
                  <span className="text-ide-text">
                    {province.coastal ? 'Yes' : 'No'}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-ide-text-muted">Continent</span>
                  <span className="text-ide-text">{province.continent}</span>
                </div>
              </div>
            </div>

            {/* State Info */}
            {state && (
              <div className="bg-ide-panel p-3 rounded">
                <h3 className="text-ide-text text-xs font-medium mb-2 flex items-center gap-2">
                  <span>🏛️</span> State
                </h3>
                <div className="space-y-2 text-xs">
                  <div className="flex justify-between">
                    <span className="text-ide-text-muted">ID</span>
                    <span className="text-ide-text">{state.id}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-ide-text-muted">Name</span>
                    <span className="text-ide-text">{state.name}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-ide-text-muted">Owner</span>
                    <span className="text-ide-text">{state.owner || 'None'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-ide-text-muted">Category</span>
                    <span className="text-ide-text capitalize">
                      {state.stateCategory}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-ide-text-muted">Manpower</span>
                    <span className="text-ide-text">
                      {state.manpower.toLocaleString()}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-ide-text-muted">Provinces</span>
                    <span className="text-ide-text">{state.provinces.length}</span>
                  </div>
                  {state.cores.length > 0 && (
                    <div className="flex justify-between">
                      <span className="text-ide-text-muted">Cores</span>
                      <span className="text-ide-text">{state.cores.join(', ')}</span>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Strategic Region Info */}
            {region && (
              <div className="bg-ide-panel p-3 rounded">
                <h3 className="text-ide-text text-xs font-medium mb-2 flex items-center gap-2">
                  <span>🌍</span> Strategic Region
                </h3>
                <div className="space-y-2 text-xs">
                  <div className="flex justify-between">
                    <span className="text-ide-text-muted">ID</span>
                    <span className="text-ide-text">{region.id}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-ide-text-muted">Name</span>
                    <span className="text-ide-text">{region.name}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-ide-text-muted">Provinces</span>
                    <span className="text-ide-text">{region.provinces.length}</span>
                  </div>
                  {region.weather.length > 0 && (
                    <div className="flex justify-between">
                      <span className="text-ide-text-muted">Weather Periods</span>
                      <span className="text-ide-text">{region.weather.length}</span>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* No State/Region */}
            {!state && province.type === 'land' && (
              <div className="bg-yellow-900/20 p-3 rounded border border-yellow-600/30">
                <div className="text-yellow-500 text-xs">
                  ⚠️ This land province is not assigned to any state
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default PropertyPanel;
