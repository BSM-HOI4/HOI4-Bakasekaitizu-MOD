import React from 'react';
import { useMapStore } from '../../stores/mapStore';
import { useProjectStore } from '../../stores/projectStore';

const StatusBar: React.FC = () => {
  const zoom = useMapStore((state) => state.zoom);
  const bmpEditor = useMapStore((state) => state.bmpEditor);
  const selectedProvinceId = useMapStore((state) => state.selectedProvinceId);
  const hoveredProvinceId = useMapStore((state) => state.hoveredProvinceId);
  const activeTool = useMapStore((state) => state.activeTool);
  
  const provinceById = useProjectStore((state) => state.provinceById);
  const stateById = useProjectStore((state) => state.stateById);
  const strategicRegionById = useProjectStore((state) => state.strategicRegionById);

  const displayProvinceId = hoveredProvinceId ?? selectedProvinceId;
  const province = displayProvinceId ? provinceById.get(displayProvinceId) : null;
  const state = province?.stateId ? stateById.get(province.stateId) : null;
  const region = province?.strategicRegionId
    ? strategicRegionById.get(province.strategicRegionId)
    : null;

  return (
    <div className="h-6 bg-ide-sidebar border-t border-ide-border flex items-center px-3 text-xs text-ide-text-muted gap-4">
      {/* Tool */}
      <div className="flex items-center gap-1">
        <span>Tool:</span>
        <span className="text-ide-text capitalize">{activeTool}</span>
      </div>

      <div className="w-px h-4 bg-ide-border" />

      {/* Province info */}
      {province && (
        <>
          <div className="flex items-center gap-1">
            <span>Province:</span>
            <span className="text-ide-text">{province.id}</span>
            <div
              className="w-3 h-3 border border-ide-border"
              style={{
                backgroundColor: `rgb(${province.color.r}, ${province.color.g}, ${province.color.b})`,
              }}
            />
          </div>

          <div className="flex items-center gap-1">
            <span>Type:</span>
            <span className="text-ide-text">{province.type}</span>
          </div>

          <div className="flex items-center gap-1">
            <span>Terrain:</span>
            <span className="text-ide-text">{province.terrain}</span>
          </div>

          {state && (
            <div className="flex items-center gap-1">
              <span>State:</span>
              <span className="text-ide-text">
                {state.id} ({state.owner || 'none'})
              </span>
            </div>
          )}

          {region && (
            <div className="flex items-center gap-1">
              <span>Region:</span>
              <span className="text-ide-text">{region.id}</span>
            </div>
          )}
        </>
      )}

      {!province && (
        <span className="text-ide-text-muted">
          Hover over map to see province info
        </span>
      )}

      <div className="flex-1" />

      {/* Image info */}
      {bmpEditor && (
        <div className="flex items-center gap-1">
          <span>
            {bmpEditor.width} × {bmpEditor.height}
          </span>
        </div>
      )}

      <div className="w-px h-4 bg-ide-border" />

      {/* Zoom */}
      <div className="flex items-center gap-1">
        <span>Zoom:</span>
        <span className="text-ide-text">{Math.round(zoom * 100)}%</span>
      </div>

      {/* Dirty indicator */}
      {bmpEditor?.isDirty && (
        <>
          <div className="w-px h-4 bg-ide-border" />
          <div className="flex items-center gap-1">
            <span className="text-ide-accent">●</span>
            <span className="text-ide-accent">Modified</span>
          </div>
        </>
      )}
    </div>
  );
};

export default StatusBar;
