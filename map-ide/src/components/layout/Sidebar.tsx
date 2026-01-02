import React, { useState, useMemo } from 'react';
import { useProjectStore } from '../../stores/projectStore';
import { useMapStore } from '../../stores/mapStore';
import { useSettingsStore } from '../../stores/settingsStore';
import ColorPalette from '../panels/ColorPalette';

type Tab = 'project' | 'colors' | 'layers' | 'selection';

const Sidebar: React.FC = () => {
  const [activeTab, setActiveTab] = useState<Tab>('colors');
  const t = useSettingsStore((state) => state.t);
  const project = useProjectStore((state) => state.project);
  const provinces = useProjectStore((state) => state.provinces);
  const states = useProjectStore((state) => state.states);
  const strategicRegions = useProjectStore((state) => state.strategicRegions);
  const aiAreas = useProjectStore((state) => state.aiAreas);
  const getStateName = useProjectStore((state) => state.getStateName);
  const getStrategicRegionName = useProjectStore((state) => state.getStrategicRegionName);
  
  const selectedProvinceId = useMapStore((state) => state.selectedProvinceId);
  const layers = useMapStore((state) => state.layers);

  // Get selected province details
  const selectedProvince = useMemo(() => {
    if (!selectedProvinceId) return null;
    return provinces.get(selectedProvinceId);
  }, [selectedProvinceId, provinces]);

  // Get state for selected province
  const selectedState = useMemo(() => {
    if (!selectedProvince?.stateId) return null;
    return states.get(selectedProvince.stateId);
  }, [selectedProvince, states]);

  // Get strategic region for selected province
  const selectedRegion = useMemo(() => {
    if (!selectedProvince?.strategicRegionId) return null;
    return strategicRegions.get(selectedProvince.strategicRegionId);
  }, [selectedProvince, strategicRegions]);
  const toggleLayer = useMapStore((state) => state.toggleLayer);
  const showGrid = useMapStore((state) => state.showGrid);
  const toggleGrid = useMapStore((state) => state.toggleGrid);
  const showBorders = useMapStore((state) => state.showBorders);
  const toggleBorders = useMapStore((state) => state.toggleBorders);

  return (
    <div className="w-64 bg-ide-sidebar border-r border-ide-border flex flex-col">
      {/* Tabs */}
      <div className="flex border-b border-ide-border flex-wrap">
        <button
          onClick={() => setActiveTab('project')}
          className={`flex-1 px-2 py-2 text-xs ${
            activeTab === 'project'
              ? 'bg-ide-panel text-ide-text border-b-2 border-ide-accent'
              : 'text-ide-text-muted hover:bg-ide-panel'
          }`}
        >
          📁
        </button>
        <button
          onClick={() => setActiveTab('colors')}
          className={`flex-1 px-2 py-2 text-xs ${
            activeTab === 'colors'
              ? 'bg-ide-panel text-ide-text border-b-2 border-ide-accent'
              : 'text-ide-text-muted hover:bg-ide-panel'
          }`}
        >
          🎨
        </button>
        <button
          onClick={() => setActiveTab('layers')}
          className={`flex-1 px-2 py-2 text-xs ${
            activeTab === 'layers'
              ? 'bg-ide-panel text-ide-text border-b-2 border-ide-accent'
              : 'text-ide-text-muted hover:bg-ide-panel'
          }`}
        >
          📚
        </button>
        <button
          onClick={() => setActiveTab('selection')}
          className={`flex-1 px-2 py-2 text-xs ${
            activeTab === 'selection'
              ? 'bg-ide-panel text-ide-text border-b-2 border-ide-accent'
              : 'text-ide-text-muted hover:bg-ide-panel'
          }`}
        >
          🔍
        </button>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-auto">
        {activeTab === 'project' && (
          <div className="p-2">
            <div className="text-ide-text-muted text-xs mb-2">プロジェクト情報</div>
            
            {project && (
              <div className="space-y-2 text-xs">
                <div className="bg-ide-panel p-2 rounded">
                  <div className="text-ide-text font-medium">統計</div>
                  <div className="mt-1 space-y-1 text-ide-text-muted">
                    <div>{t.provinces}: {provinces.size}</div>
                    <div>{t.states}: {states.size}</div>
                    <div>{t.strategicRegions}: {strategicRegions.size}</div>
                    <div>{t.aiAreas}: {aiAreas.length}</div>
                  </div>
                </div>

                <div className="bg-ide-panel p-2 rounded">
                  <div className="text-ide-text font-medium">プロヴィンスタイプ</div>
                  <div className="mt-1 space-y-1 text-ide-text-muted">
                    <div>
                      陸地: {Array.from(provinces.values()).filter((p) => p.type === 'land').length}
                    </div>
                    <div>
                      海: {Array.from(provinces.values()).filter((p) => p.type === 'sea').length}
                    </div>
                    <div>
                      湖: {Array.from(provinces.values()).filter((p) => p.type === 'lake').length}
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'colors' && <ColorPalette />}

        {activeTab === 'layers' && (
          <div className="p-2">
            <div className="text-ide-text-muted text-xs mb-2">レイヤー表示</div>
            
            <div className="space-y-1">
              <label className="flex items-center gap-2 p-2 hover:bg-ide-panel rounded cursor-pointer">
                <input
                  type="checkbox"
                  checked={layers.provinces}
                  onChange={() => toggleLayer('provinces')}
                  className="accent-ide-accent"
                />
                <span className="text-ide-text text-xs">{t.provinces}</span>
              </label>
              
              <label className="flex items-center gap-2 p-2 hover:bg-ide-panel rounded cursor-pointer">
                <input
                  type="checkbox"
                  checked={layers.states}
                  onChange={() => toggleLayer('states')}
                  className="accent-ide-accent"
                />
                <span className="text-ide-text text-xs">{t.states}</span>
              </label>
              
              <label className="flex items-center gap-2 p-2 hover:bg-ide-panel rounded cursor-pointer">
                <input
                  type="checkbox"
                  checked={layers.strategicRegions}
                  onChange={() => toggleLayer('strategicRegions')}
                  className="accent-ide-accent"
                />
                <span className="text-ide-text text-xs">{t.strategicRegions}</span>
              </label>
              
              <label className="flex items-center gap-2 p-2 hover:bg-ide-panel rounded cursor-pointer">
                <input
                  type="checkbox"
                  checked={layers.aiAreas}
                  onChange={() => toggleLayer('aiAreas')}
                  className="accent-ide-accent"
                />
                <span className="text-ide-text text-xs">{t.aiAreas}</span>
              </label>
              
              <label className="flex items-center gap-2 p-2 hover:bg-ide-panel rounded cursor-pointer">
                <input
                  type="checkbox"
                  checked={layers.terrain}
                  onChange={() => toggleLayer('terrain')}
                  className="accent-ide-accent"
                />
                <span className="text-ide-text text-xs">{t.terrain}</span>
              </label>

              <div className="h-px bg-ide-border my-2" />

              <label className="flex items-center gap-2 p-2 hover:bg-ide-panel rounded cursor-pointer">
                <input
                  type="checkbox"
                  checked={showGrid}
                  onChange={toggleGrid}
                  className="accent-ide-accent"
                />
                <span className="text-ide-text text-xs">{t.showGrid}</span>
              </label>
              
              <label className="flex items-center gap-2 p-2 hover:bg-ide-panel rounded cursor-pointer">
                <input
                  type="checkbox"
                  checked={showBorders}
                  onChange={toggleBorders}
                  className="accent-ide-accent"
                />
                <span className="text-ide-text text-xs">{t.showBorders}</span>
              </label>
            </div>
          </div>
        )}

        {activeTab === 'selection' && (
          <div className="p-2">
            <div className="text-ide-text-muted text-xs mb-2">選択情報</div>
            
            {!selectedProvince ? (
              <div className="text-ide-text-muted text-xs p-2">
                マップ上でプロヴィンスを選択してください
              </div>
            ) : (
              <div className="space-y-2">
                {/* Province Info */}
                <div className="bg-ide-panel p-2 rounded">
                  <div className="text-ide-text font-medium text-sm flex items-center gap-1">
                    🟡 {t.provinces}
                  </div>
                  <div className="mt-1 space-y-1 text-ide-text-muted text-xs">
                    <div><span className="text-ide-text">ID:</span> {selectedProvince.id}</div>
                    <div>
                      <span className="text-ide-text">色:</span>{' '}
                      <span 
                        className="inline-block w-3 h-3 rounded"
                        style={{ 
                          backgroundColor: `rgb(${selectedProvince.color.r},${selectedProvince.color.g},${selectedProvince.color.b})`,
                          verticalAlign: 'middle'
                        }}
                      />
                      {' '}({selectedProvince.color.r}, {selectedProvince.color.g}, {selectedProvince.color.b})
                    </div>
                    <div><span className="text-ide-text">タイプ:</span> {selectedProvince.type}</div>
                    <div><span className="text-ide-text">地形:</span> {selectedProvince.terrain}</div>
                    {selectedProvince.coastal && (
                      <div className="text-blue-400">🌊 沿岸プロヴィンス</div>
                    )}
                  </div>
                </div>

                {/* State Info */}
                {selectedState && (
                  <div className="bg-ide-panel p-2 rounded">
                    <div className="text-ide-text font-medium text-sm flex items-center gap-1">
                      🟠 {t.states}
                    </div>
                    <div className="mt-1 space-y-1 text-ide-text-muted text-xs">
                      <div><span className="text-ide-text">ID:</span> {selectedState.id}</div>
                      <div>
                        <span className="text-ide-text">名前:</span>{' '}
                        <span className="text-yellow-300">{getStateName(selectedState.id)}</span>
                      </div>
                      <div><span className="text-ide-text">カテゴリ:</span> {selectedState.stateCategory}</div>
                      <div><span className="text-ide-text">人口:</span> {selectedState.manpower?.toLocaleString() || 0}</div>
                      <div><span className="text-ide-text">プロヴィンス数:</span> {selectedState.provinces.length}</div>
                      {selectedState.owner && (
                        <div><span className="text-ide-text">所有者:</span> {selectedState.owner}</div>
                      )}
                    </div>
                  </div>
                )}

                {/* Strategic Region Info */}
                {selectedRegion && (
                  <div className="bg-ide-panel p-2 rounded">
                    <div className="text-ide-text font-medium text-sm flex items-center gap-1">
                      🔵 {t.strategicRegions}
                    </div>
                    <div className="mt-1 space-y-1 text-ide-text-muted text-xs">
                      <div><span className="text-ide-text">ID:</span> {selectedRegion.id}</div>
                      <div>
                        <span className="text-ide-text">名前:</span>{' '}
                        <span className="text-cyan-300">{getStrategicRegionName(selectedRegion.id)}</span>
                      </div>
                      <div><span className="text-ide-text">プロヴィンス数:</span> {selectedRegion.provinces.length}</div>
                      {selectedRegion.weather && selectedRegion.weather.length > 0 && (
                        <div><span className="text-ide-text">天候期間数:</span> {selectedRegion.weather.length}</div>
                      )}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Sidebar;
