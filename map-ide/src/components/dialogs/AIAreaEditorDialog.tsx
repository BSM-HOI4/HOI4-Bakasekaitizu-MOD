/**
 * AI Area Editor Dialog
 * 
 * Dialog for editing AI area properties including
 * strategic region and continent assignments.
 */

import React, { useState, useEffect, useMemo, useCallback } from 'react';
import { useProjectStore } from '../../stores/projectStore';
import { AIArea } from '../../types';

interface AIAreaEditorDialogProps {
  isOpen: boolean;
  onClose: () => void;
  areaName: string;
}

const CONTINENTS = [
  'europe',
  'north_america', 
  'south_america',
  'africa',
  'asia',
  'middle_east',
  'oceania',
  'antarctica',
];

const AIAreaEditorDialog: React.FC<AIAreaEditorDialogProps> = ({
  isOpen,
  onClose,
  areaName,
}) => {
  const aiAreas = useProjectStore((state) => state.aiAreas);
  const strategicRegions = useProjectStore((state) => state.strategicRegions);
  const updateAIArea = useProjectStore((state) => state.updateAIArea);
  const saveAIAreas = useProjectStore((state) => state.saveAIAreas);

  const areaData = useMemo(() => 
    aiAreas.find(a => a.name === areaName),
    [aiAreas, areaName]
  );

  // Form state
  const [formData, setFormData] = useState<{
    name: string;
    strategicRegions: number[];
    continents: string[];
  }>({
    name: '',
    strategicRegions: [],
    continents: [],
  });

  const [searchTerm, setSearchTerm] = useState('');
  const [isSaving, setIsSaving] = useState(false);
  const [saveMessage, setSaveMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  // Initialize form data
  useEffect(() => {
    if (!isOpen || !areaData) return;

    setFormData({
      name: areaData.name,
      strategicRegions: [...(areaData.strategicRegions || [])],
      continents: [...(areaData.continents || [])],
    });
    setSearchTerm('');
    setSaveMessage(null);
  }, [isOpen, areaData]);

  // Get strategic region details
  const assignedRegionsWithNames = useMemo(() => {
    return formData.strategicRegions.map(id => {
      const region = strategicRegions.get(id);
      return { id, name: region?.name || `Region ${id}` };
    });
  }, [formData.strategicRegions, strategicRegions]);

  // Get available (unassigned) strategic regions
  const availableRegions = useMemo(() => {
    const usedRegions = new Set<number>();
    for (const area of aiAreas) {
      if (area.name !== areaName && area.strategicRegions) {
        area.strategicRegions.forEach(id => usedRegions.add(id));
      }
    }
    
    return Array.from(strategicRegions.values())
      .filter(r => !usedRegions.has(r.id) && !formData.strategicRegions.includes(r.id))
      .filter(r => 
        searchTerm === '' || 
        r.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        r.id.toString().includes(searchTerm)
      )
      .sort((a, b) => a.id - b.id);
  }, [strategicRegions, aiAreas, areaName, formData.strategicRegions, searchTerm]);

  // Handle save
  const handleSave = useCallback(async () => {
    if (!areaData) return;

    setIsSaving(true);
    setSaveMessage(null);

    const updatedArea: AIArea = {
      ...areaData,
      strategicRegions: formData.strategicRegions,
      continents: formData.continents,
    };

    updateAIArea(updatedArea);
    
    const success = await saveAIAreas();
    
    setIsSaving(false);
    setSaveMessage({
      type: success ? 'success' : 'error',
      text: success ? 'AI area saved successfully!' : 'Failed to save AI areas file',
    });
  }, [areaData, formData, updateAIArea, saveAIAreas]);

  // Handle add strategic region
  const handleAddRegion = useCallback((regionId: number) => {
    setFormData(prev => ({
      ...prev,
      strategicRegions: [...prev.strategicRegions, regionId],
    }));
  }, []);

  // Handle remove strategic region
  const handleRemoveRegion = useCallback((regionId: number) => {
    setFormData(prev => ({
      ...prev,
      strategicRegions: prev.strategicRegions.filter(id => id !== regionId),
    }));
  }, []);

  // Handle toggle continent
  const handleToggleContinent = useCallback((continent: string) => {
    setFormData(prev => {
      const hasContinent = prev.continents.includes(continent);
      return {
        ...prev,
        continents: hasContinent
          ? prev.continents.filter(c => c !== continent)
          : [...prev.continents, continent],
      };
    });
  }, []);

  if (!isOpen || !areaData) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-ide-sidebar rounded-lg shadow-xl w-[700px] max-h-[90vh] overflow-hidden border border-ide-border">
        {/* Header */}
        <div className="px-4 py-3 border-b border-ide-border flex items-center justify-between">
          <h2 className="text-lg font-semibold text-ide-text">
            Edit AI Area: {areaName}
          </h2>
          <button
            onClick={onClose}
            className="text-ide-text-muted hover:text-ide-text transition-colors"
          >
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Content */}
        <div className="p-4 space-y-4 overflow-y-auto max-h-[65vh]">
          {/* Save message */}
          {saveMessage && (
            <div className={`p-3 rounded ${
              saveMessage.type === 'success' 
                ? 'bg-green-900/30 border border-green-500/50 text-green-400'
                : 'bg-red-900/30 border border-red-500/50 text-red-400'
            }`}>
              {saveMessage.text}
            </div>
          )}

          {/* Continents */}
          <div>
            <label className="block text-sm font-medium text-ide-text-muted mb-2">
              Continents
            </label>
            <div className="flex flex-wrap gap-2">
              {CONTINENTS.map(continent => (
                <button
                  key={continent}
                  onClick={() => handleToggleContinent(continent)}
                  className={`px-3 py-1.5 rounded text-sm transition-colors ${
                    formData.continents.includes(continent)
                      ? 'bg-magenta-600 text-white'
                      : 'bg-ide-hover text-ide-text hover:bg-ide-active'
                  }`}
                  style={formData.continents.includes(continent) ? { backgroundColor: '#c026d3' } : {}}
                >
                  {continent.replace(/_/g, ' ')}
                </button>
              ))}
            </div>
          </div>

          {/* Assigned Strategic Regions */}
          <div>
            <label className="block text-sm font-medium text-ide-text-muted mb-2">
              Assigned Strategic Regions ({formData.strategicRegions.length})
            </label>
            <div className="bg-ide-bg rounded border border-ide-border p-2 max-h-40 overflow-y-auto">
              {assignedRegionsWithNames.length > 0 ? (
                <div className="space-y-1">
                  {assignedRegionsWithNames.map(({ id, name }) => (
                    <div
                      key={id}
                      className="flex items-center justify-between px-2 py-1 bg-ide-hover rounded"
                    >
                      <span className="text-sm text-ide-text">
                        <span className="text-cyan-400">#{id}</span> {name}
                      </span>
                      <button
                        onClick={() => handleRemoveRegion(id)}
                        className="text-red-400 hover:text-red-300 px-1"
                      >
                        ×
                      </button>
                    </div>
                  ))}
                </div>
              ) : (
                <span className="text-ide-text-muted text-sm">No strategic regions assigned</span>
              )}
            </div>
          </div>

          {/* Add Strategic Regions */}
          <div>
            <label className="block text-sm font-medium text-ide-text-muted mb-2">
              Add Strategic Regions
            </label>
            <input
              type="text"
              placeholder="Search by name or ID..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full px-3 py-2 mb-2 bg-ide-bg border border-ide-border rounded text-ide-text"
            />
            <div className="bg-ide-bg rounded border border-ide-border p-2 max-h-40 overflow-y-auto">
              {availableRegions.length > 0 ? (
                <div className="space-y-1">
                  {availableRegions.slice(0, 50).map(region => (
                    <button
                      key={region.id}
                      onClick={() => handleAddRegion(region.id)}
                      className="w-full flex items-center justify-between px-2 py-1 
                               hover:bg-ide-hover rounded text-left transition-colors"
                    >
                      <span className="text-sm text-ide-text">
                        <span className="text-cyan-400">#{region.id}</span> {region.name}
                      </span>
                      <span className="text-xs text-green-400">+ Add</span>
                    </button>
                  ))}
                  {availableRegions.length > 50 && (
                    <div className="text-center text-xs text-ide-text-muted py-1">
                      ...and {availableRegions.length - 50} more
                    </div>
                  )}
                </div>
              ) : (
                <span className="text-ide-text-muted text-sm">
                  {searchTerm ? 'No matching regions found' : 'No available regions'}
                </span>
              )}
            </div>
          </div>

          {/* Statistics */}
          <div className="bg-ide-bg rounded border border-ide-border p-3">
            <h3 className="text-sm font-medium text-ide-text mb-2">Statistics</h3>
            <div className="grid grid-cols-2 gap-2 text-sm">
              <div className="flex justify-between">
                <span className="text-ide-text-muted">Strategic Regions:</span>
                <span className="text-ide-text">{formData.strategicRegions.length}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-ide-text-muted">Continents:</span>
                <span className="text-ide-text">{formData.continents.length}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-ide-text-muted">Total Provinces:</span>
                <span className="text-ide-text">
                  {formData.strategicRegions.reduce((sum, id) => {
                    const region = strategicRegions.get(id);
                    return sum + (region?.provinces.length || 0);
                  }, 0)}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="px-4 py-3 border-t border-ide-border flex items-center justify-between">
          <div className="text-xs text-ide-text-muted">
            {areaData.filePath && `File: ${areaData.filePath.split('/').pop()}`}
          </div>
          <div className="flex gap-2">
            <button
              onClick={onClose}
              className="px-4 py-2 bg-ide-hover hover:bg-ide-active text-ide-text rounded"
            >
              Close
            </button>
            <button
              onClick={handleSave}
              disabled={isSaving}
              className="px-4 py-2 text-white rounded disabled:cursor-wait"
              style={{ backgroundColor: isSaving ? '#9333ea' : '#c026d3' }}
              onMouseEnter={(e) => !isSaving && (e.currentTarget.style.backgroundColor = '#a21caf')}
              onMouseLeave={(e) => !isSaving && (e.currentTarget.style.backgroundColor = '#c026d3')}
            >
              {isSaving ? 'Saving...' : 'Save Changes'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AIAreaEditorDialog;
