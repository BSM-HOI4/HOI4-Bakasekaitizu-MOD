/**
 * State Editor Dialog
 * 
 * Dialog for editing state properties, managing province assignments,
 * and handling buildings and victory points.
 */

import React, { useState, useEffect, useMemo, useCallback } from 'react';
import { useProjectStore } from '../../stores/projectStore';
import { useMapStore } from '../../stores/mapStore';
import { State, Province } from '../../types';

interface StateEditorDialogProps {
  isOpen: boolean;
  onClose: () => void;
  stateId: number;
}

const STATE_CATEGORIES = [
  'wasteland', 'enclave', 'tiny_island', 'pastoral', 'small_island',
  'rural', 'town', 'large_town', 'city', 'large_city', 'metropolis', 'megalopolis'
];

const StateEditorDialog: React.FC<StateEditorDialogProps> = ({
  isOpen,
  onClose,
  stateId,
}) => {
  const states = useProjectStore((state) => state.states);
  const provinces = useProjectStore((state) => state.provinces);
  const updateState = useProjectStore((state) => state.updateState);
  const saveState = useProjectStore((state) => state.saveState);
  const addProvinceToState = useProjectStore((state) => state.addProvinceToState);
  const removeProvinceFromState = useProjectStore((state) => state.removeProvinceFromState);
  
  const selectedProvinceId = useMapStore((state) => state.selectedProvinceId);

  const stateData = states.get(stateId);

  // Form state
  const [formData, setFormData] = useState<{
    name: string;
    manpower: number;
    stateCategory: string;
    owner: string;
    cores: string[];
    localSupplies: number;
  }>({
    name: '',
    manpower: 0,
    stateCategory: 'rural',
    owner: '',
    cores: [],
    localSupplies: 0,
  });

  const [coreInput, setCoreInput] = useState('');
  const [isSaving, setIsSaving] = useState(false);
  const [saveMessage, setSaveMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  // Initialize form data
  useEffect(() => {
    if (!isOpen || !stateData) return;

    setFormData({
      name: stateData.name,
      manpower: stateData.manpower,
      stateCategory: stateData.stateCategory,
      owner: stateData.owner,
      cores: [...stateData.cores],
      localSupplies: stateData.localSupplies,
    });
    setSaveMessage(null);
  }, [isOpen, stateData]);

  // Get assigned provinces
  const assignedProvinces = useMemo(() => {
    if (!stateData) return [];
    return stateData.provinces
      .map(id => provinces.get(id))
      .filter((p): p is Province => p !== undefined);
  }, [stateData, provinces]);

  // Get unassigned land provinces
  const unassignedProvinces = useMemo(() => {
    return Array.from(provinces.values())
      .filter(p => p.type === 'land' && !p.stateId)
      .sort((a, b) => a.id - b.id);
  }, [provinces]);

  // Handle save
  const handleSave = useCallback(async () => {
    if (!stateData) return;

    setIsSaving(true);
    setSaveMessage(null);

    const updatedState: State = {
      ...stateData,
      name: formData.name,
      manpower: formData.manpower,
      stateCategory: formData.stateCategory,
      owner: formData.owner,
      cores: formData.cores,
      localSupplies: formData.localSupplies,
    };

    updateState(updatedState);
    
    const success = await saveState(stateId);
    
    setIsSaving(false);
    setSaveMessage({
      type: success ? 'success' : 'error',
      text: success ? 'State saved successfully!' : 'Failed to save state file',
    });
  }, [stateData, formData, stateId, updateState, saveState]);

  // Handle add core
  const handleAddCore = useCallback(() => {
    const tag = coreInput.trim().toUpperCase();
    if (tag && tag.length === 3 && !formData.cores.includes(tag)) {
      setFormData(prev => ({ ...prev, cores: [...prev.cores, tag] }));
      setCoreInput('');
    }
  }, [coreInput, formData.cores]);

  // Handle remove core
  const handleRemoveCore = useCallback((tag: string) => {
    setFormData(prev => ({ 
      ...prev, 
      cores: prev.cores.filter(c => c !== tag) 
    }));
  }, []);

  // Handle add province
  const handleAddProvince = useCallback((provinceId: number) => {
    addProvinceToState(stateId, provinceId);
  }, [stateId, addProvinceToState]);

  // Handle remove province
  const handleRemoveProvince = useCallback((provinceId: number) => {
    removeProvinceFromState(stateId, provinceId);
  }, [stateId, removeProvinceFromState]);

  // Handle add selected province
  const handleAddSelectedProvince = useCallback(() => {
    if (selectedProvinceId) {
      const prov = provinces.get(selectedProvinceId);
      if (prov && prov.type === 'land' && !prov.stateId) {
        handleAddProvince(selectedProvinceId);
      }
    }
  }, [selectedProvinceId, provinces, handleAddProvince]);

  if (!isOpen || !stateData) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-ide-sidebar rounded-lg shadow-xl w-[700px] max-h-[90vh] overflow-hidden border border-ide-border">
        {/* Header */}
        <div className="px-4 py-3 border-b border-ide-border flex items-center justify-between">
          <h2 className="text-lg font-semibold text-ide-text">
            Edit State #{stateId}
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
        <div className="p-4 space-y-4 overflow-y-auto max-h-[60vh]">
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

          {/* Basic Info */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-ide-text-muted mb-1">
                State Name (Localisation Key)
              </label>
              <input
                type="text"
                value={formData.name}
                onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
                className="w-full px-3 py-2 bg-ide-bg border border-ide-border rounded text-ide-text"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-ide-text-muted mb-1">
                Owner (Country Tag)
              </label>
              <input
                type="text"
                value={formData.owner}
                onChange={(e) => setFormData(prev => ({ 
                  ...prev, 
                  owner: e.target.value.toUpperCase().slice(0, 3) 
                }))}
                maxLength={3}
                placeholder="e.g., GER"
                className="w-full px-3 py-2 bg-ide-bg border border-ide-border rounded text-ide-text uppercase"
              />
            </div>
          </div>

          <div className="grid grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-ide-text-muted mb-1">
                Category
              </label>
              <select
                value={formData.stateCategory}
                onChange={(e) => setFormData(prev => ({ ...prev, stateCategory: e.target.value }))}
                className="w-full px-3 py-2 bg-ide-bg border border-ide-border rounded text-ide-text"
              >
                {STATE_CATEGORIES.map(cat => (
                  <option key={cat} value={cat}>
                    {cat.replace(/_/g, ' ')}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-ide-text-muted mb-1">
                Manpower
              </label>
              <input
                type="number"
                value={formData.manpower}
                onChange={(e) => setFormData(prev => ({ 
                  ...prev, 
                  manpower: parseInt(e.target.value) || 0 
                }))}
                className="w-full px-3 py-2 bg-ide-bg border border-ide-border rounded text-ide-text"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-ide-text-muted mb-1">
                Local Supplies
              </label>
              <input
                type="number"
                step="0.1"
                value={formData.localSupplies}
                onChange={(e) => setFormData(prev => ({ 
                  ...prev, 
                  localSupplies: parseFloat(e.target.value) || 0 
                }))}
                className="w-full px-3 py-2 bg-ide-bg border border-ide-border rounded text-ide-text"
              />
            </div>
          </div>

          {/* Cores */}
          <div>
            <label className="block text-sm font-medium text-ide-text-muted mb-1">
              Core Countries
            </label>
            <div className="flex gap-2 mb-2">
              <input
                type="text"
                value={coreInput}
                onChange={(e) => setCoreInput(e.target.value.toUpperCase().slice(0, 3))}
                maxLength={3}
                placeholder="TAG"
                className="w-24 px-3 py-1 bg-ide-bg border border-ide-border rounded text-ide-text uppercase"
                onKeyPress={(e) => e.key === 'Enter' && handleAddCore()}
              />
              <button
                onClick={handleAddCore}
                className="px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white rounded text-sm"
              >
                Add Core
              </button>
            </div>
            <div className="flex flex-wrap gap-2">
              {formData.cores.map(tag => (
                <span
                  key={tag}
                  className="px-2 py-1 bg-ide-hover rounded text-sm text-ide-text flex items-center gap-1"
                >
                  {tag}
                  <button
                    onClick={() => handleRemoveCore(tag)}
                    className="text-red-400 hover:text-red-300"
                  >
                    ×
                  </button>
                </span>
              ))}
              {formData.cores.length === 0 && (
                <span className="text-ide-text-muted text-sm">No cores assigned</span>
              )}
            </div>
          </div>

          {/* Provinces */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <label className="block text-sm font-medium text-ide-text-muted">
                Assigned Provinces ({assignedProvinces.length})
              </label>
              {selectedProvinceId && (
                <button
                  onClick={handleAddSelectedProvince}
                  disabled={
                    !provinces.get(selectedProvinceId) ||
                    provinces.get(selectedProvinceId)?.type !== 'land' ||
                    provinces.get(selectedProvinceId)?.stateId !== undefined
                  }
                  className="px-2 py-1 bg-green-600 hover:bg-green-700 disabled:bg-gray-600 
                           disabled:cursor-not-allowed text-white rounded text-xs"
                >
                  Add Selected (#{selectedProvinceId})
                </button>
              )}
            </div>
            <div className="bg-ide-bg rounded border border-ide-border p-2 max-h-32 overflow-y-auto">
              <div className="flex flex-wrap gap-1">
                {assignedProvinces.map(prov => (
                  <span
                    key={prov.id}
                    className="px-2 py-0.5 bg-ide-hover rounded text-xs text-ide-text flex items-center gap-1"
                  >
                    {prov.id}
                    <button
                      onClick={() => handleRemoveProvince(prov.id)}
                      className="text-red-400 hover:text-red-300"
                    >
                      ×
                    </button>
                  </span>
                ))}
                {assignedProvinces.length === 0 && (
                  <span className="text-ide-text-muted text-xs">No provinces assigned</span>
                )}
              </div>
            </div>
          </div>

          {/* Unassigned Provinces */}
          {unassignedProvinces.length > 0 && (
            <div>
              <label className="block text-sm font-medium text-ide-text-muted mb-2">
                Unassigned Land Provinces ({unassignedProvinces.length})
              </label>
              <div className="bg-ide-bg rounded border border-ide-border p-2 max-h-24 overflow-y-auto">
                <div className="flex flex-wrap gap-1">
                  {unassignedProvinces.slice(0, 100).map(prov => (
                    <button
                      key={prov.id}
                      onClick={() => handleAddProvince(prov.id)}
                      className="px-2 py-0.5 bg-yellow-900/30 hover:bg-yellow-800/50 
                               border border-yellow-600/30 rounded text-xs text-yellow-400"
                    >
                      +{prov.id}
                    </button>
                  ))}
                  {unassignedProvinces.length > 100 && (
                    <span className="text-ide-text-muted text-xs">
                      ...and {unassignedProvinces.length - 100} more
                    </span>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Victory Points */}
          <div>
            <label className="block text-sm font-medium text-ide-text-muted mb-2">
              Victory Points
            </label>
            <div className="bg-ide-bg rounded border border-ide-border p-2">
              {stateData.victoryPoints.length > 0 ? (
                <div className="space-y-1">
                  {stateData.victoryPoints.map((vp, i) => (
                    <div key={i} className="flex items-center gap-2 text-sm">
                      <span className="text-ide-text-muted">Province {vp.provinceId}:</span>
                      <span className="text-ide-text font-medium">{vp.value} VP</span>
                    </div>
                  ))}
                </div>
              ) : (
                <span className="text-ide-text-muted text-sm">No victory points</span>
              )}
            </div>
          </div>

          {/* Buildings */}
          <div>
            <label className="block text-sm font-medium text-ide-text-muted mb-2">
              Buildings
            </label>
            <div className="bg-ide-bg rounded border border-ide-border p-2">
              {stateData.buildings.length > 0 ? (
                <div className="grid grid-cols-2 gap-2 text-sm">
                  {stateData.buildings.map((b, i) => (
                    <div key={i} className="flex items-center justify-between">
                      <span className="text-ide-text-muted">
                        {b.type.replace(/_/g, ' ')}
                        {b.provinceId && ` (${b.provinceId})`}:
                      </span>
                      <span className="text-ide-text font-medium">{b.level}</span>
                    </div>
                  ))}
                </div>
              ) : (
                <span className="text-ide-text-muted text-sm">No buildings</span>
              )}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="px-4 py-3 border-t border-ide-border flex items-center justify-between">
          <div className="text-xs text-ide-text-muted">
            {stateData.filePath && `File: ${stateData.filePath.split('/').pop()}`}
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
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800 
                       disabled:cursor-wait text-white rounded"
            >
              {isSaving ? 'Saving...' : 'Save Changes'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StateEditorDialog;
