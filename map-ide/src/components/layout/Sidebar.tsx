import React, { useState } from 'react';
import { useProjectStore } from '../../stores/projectStore';
import { useMapStore } from '../../stores/mapStore';
import ColorPalette from '../panels/ColorPalette';

type Tab = 'project' | 'colors' | 'layers';

const Sidebar: React.FC = () => {
  const [activeTab, setActiveTab] = useState<Tab>('colors');
  const project = useProjectStore((state) => state.project);
  const provinces = useProjectStore((state) => state.provinces);
  const states = useProjectStore((state) => state.states);
  const strategicRegions = useProjectStore((state) => state.strategicRegions);
  const aiAreas = useProjectStore((state) => state.aiAreas);
  
  const layers = useMapStore((state) => state.layers);
  const toggleLayer = useMapStore((state) => state.toggleLayer);
  const showGrid = useMapStore((state) => state.showGrid);
  const toggleGrid = useMapStore((state) => state.toggleGrid);
  const showBorders = useMapStore((state) => state.showBorders);
  const toggleBorders = useMapStore((state) => state.toggleBorders);

  return (
    <div className="w-64 bg-ide-sidebar border-r border-ide-border flex flex-col">
      {/* Tabs */}
      <div className="flex border-b border-ide-border">
        <button
          onClick={() => setActiveTab('project')}
          className={`flex-1 px-3 py-2 text-xs ${
            activeTab === 'project'
              ? 'bg-ide-panel text-ide-text border-b-2 border-ide-accent'
              : 'text-ide-text-muted hover:bg-ide-panel'
          }`}
        >
          Project
        </button>
        <button
          onClick={() => setActiveTab('colors')}
          className={`flex-1 px-3 py-2 text-xs ${
            activeTab === 'colors'
              ? 'bg-ide-panel text-ide-text border-b-2 border-ide-accent'
              : 'text-ide-text-muted hover:bg-ide-panel'
          }`}
        >
          Colors
        </button>
        <button
          onClick={() => setActiveTab('layers')}
          className={`flex-1 px-3 py-2 text-xs ${
            activeTab === 'layers'
              ? 'bg-ide-panel text-ide-text border-b-2 border-ide-accent'
              : 'text-ide-text-muted hover:bg-ide-panel'
          }`}
        >
          Layers
        </button>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-auto">
        {activeTab === 'project' && (
          <div className="p-2">
            <div className="text-ide-text-muted text-xs mb-2">Project Info</div>
            
            {project && (
              <div className="space-y-2 text-xs">
                <div className="bg-ide-panel p-2 rounded">
                  <div className="text-ide-text font-medium">Statistics</div>
                  <div className="mt-1 space-y-1 text-ide-text-muted">
                    <div>Provinces: {provinces.length}</div>
                    <div>States: {states.length}</div>
                    <div>Strategic Regions: {strategicRegions.length}</div>
                    <div>AI Areas: {aiAreas.length}</div>
                  </div>
                </div>

                <div className="bg-ide-panel p-2 rounded">
                  <div className="text-ide-text font-medium">Province Types</div>
                  <div className="mt-1 space-y-1 text-ide-text-muted">
                    <div>
                      Land: {provinces.filter((p) => p.type === 'land').length}
                    </div>
                    <div>
                      Sea: {provinces.filter((p) => p.type === 'sea').length}
                    </div>
                    <div>
                      Lake: {provinces.filter((p) => p.type === 'lake').length}
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
            <div className="text-ide-text-muted text-xs mb-2">Layer Visibility</div>
            
            <div className="space-y-1">
              <label className="flex items-center gap-2 p-2 hover:bg-ide-panel rounded cursor-pointer">
                <input
                  type="checkbox"
                  checked={layers.provinces}
                  onChange={() => toggleLayer('provinces')}
                  className="accent-ide-accent"
                />
                <span className="text-ide-text text-xs">Provinces</span>
              </label>
              
              <label className="flex items-center gap-2 p-2 hover:bg-ide-panel rounded cursor-pointer">
                <input
                  type="checkbox"
                  checked={layers.states}
                  onChange={() => toggleLayer('states')}
                  className="accent-ide-accent"
                />
                <span className="text-ide-text text-xs">States</span>
              </label>
              
              <label className="flex items-center gap-2 p-2 hover:bg-ide-panel rounded cursor-pointer">
                <input
                  type="checkbox"
                  checked={layers.strategicRegions}
                  onChange={() => toggleLayer('strategicRegions')}
                  className="accent-ide-accent"
                />
                <span className="text-ide-text text-xs">Strategic Regions</span>
              </label>
              
              <label className="flex items-center gap-2 p-2 hover:bg-ide-panel rounded cursor-pointer">
                <input
                  type="checkbox"
                  checked={layers.aiAreas}
                  onChange={() => toggleLayer('aiAreas')}
                  className="accent-ide-accent"
                />
                <span className="text-ide-text text-xs">AI Areas</span>
              </label>
              
              <label className="flex items-center gap-2 p-2 hover:bg-ide-panel rounded cursor-pointer">
                <input
                  type="checkbox"
                  checked={layers.terrain}
                  onChange={() => toggleLayer('terrain')}
                  className="accent-ide-accent"
                />
                <span className="text-ide-text text-xs">Terrain</span>
              </label>

              <div className="h-px bg-ide-border my-2" />

              <label className="flex items-center gap-2 p-2 hover:bg-ide-panel rounded cursor-pointer">
                <input
                  type="checkbox"
                  checked={showGrid}
                  onChange={toggleGrid}
                  className="accent-ide-accent"
                />
                <span className="text-ide-text text-xs">Pixel Grid</span>
              </label>
              
              <label className="flex items-center gap-2 p-2 hover:bg-ide-panel rounded cursor-pointer">
                <input
                  type="checkbox"
                  checked={showBorders}
                  onChange={toggleBorders}
                  className="accent-ide-accent"
                />
                <span className="text-ide-text text-xs">Province Borders</span>
              </label>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Sidebar;
