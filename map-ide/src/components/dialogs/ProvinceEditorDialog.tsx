/**
 * Province Editor Dialog
 * 
 * Dialog for creating new provinces, editing existing provinces,
 * and managing province properties.
 */

import React, { useState, useEffect, useMemo, useCallback } from 'react';
import { useProjectStore } from '../../stores/projectStore';
import { useMapStore } from '../../stores/mapStore';
import { Province, ProvinceType, TerrainType, RGB } from '../../types';
import { rgbToHex, rgbToKey, generateUniqueColor } from '../../utils/colorUtils';

interface ProvinceEditorDialogProps {
  isOpen: boolean;
  onClose: () => void;
  mode: 'create' | 'edit';
  provinceId?: number;
}

const PROVINCE_TYPES: ProvinceType[] = ['land', 'sea', 'lake'];
const TERRAIN_TYPES: TerrainType[] = [
  'plains', 'forest', 'hills', 'mountain', 'urban', 
  'jungle', 'marsh', 'desert', 'ocean', 'lakes', 'unknown'
];

const ProvinceEditorDialog: React.FC<ProvinceEditorDialogProps> = ({
  isOpen,
  onClose,
  mode,
  provinceId,
}) => {
  const provinces = useProjectStore((state) => state.provinces);
  const addProvince = useProjectStore((state) => state.addProvince);
  const updateProvince = useProjectStore((state) => state.updateProvince);
  const deleteProvince = useProjectStore((state) => state.deleteProvince);
  
  const setSelectedColor = useMapStore((state) => state.setSelectedColor);

  // Form state
  const [formData, setFormData] = useState<{
    id: number;
    color: RGB;
    type: ProvinceType;
    coastal: boolean;
    terrain: TerrainType;
    continent: number;
  }>({
    id: 1,
    color: { r: 128, g: 128, b: 128 },
    type: 'land',
    coastal: false,
    terrain: 'plains',
    continent: 0,
  });

  const [errors, setErrors] = useState<string[]>([]);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  // Get used colors
  const usedColors = useMemo(() => {
    const colors = new Set<string>();
    for (const prov of provinces.values()) {
      if (mode === 'edit' && prov.id === provinceId) continue;
      colors.add(rgbToKey(prov.color));
    }
    return colors;
  }, [provinces, mode, provinceId]);

  // Get used IDs
  const usedIds = useMemo(() => {
    const ids = new Set<number>();
    for (const prov of provinces.values()) {
      ids.add(prov.id);
    }
    return ids;
  }, [provinces]);

  // Get next available ID
  const nextAvailableId = useMemo(() => {
    let id = 1;
    while (usedIds.has(id)) {
      id++;
    }
    return id;
  }, [usedIds]);

  // Initialize form data
  useEffect(() => {
    if (!isOpen) return;

    if (mode === 'create') {
      const newColor = generateUniqueColor(usedColors);
      setFormData({
        id: nextAvailableId,
        color: newColor,
        type: 'land',
        coastal: false,
        terrain: 'plains',
        continent: 0,
      });
    } else if (mode === 'edit' && provinceId) {
      const province = provinces.get(provinceId);
      if (province) {
        setFormData({
          id: province.id,
          color: { ...province.color },
          type: province.type,
          coastal: province.coastal,
          terrain: province.terrain,
          continent: province.continent,
        });
      }
    }
    setErrors([]);
    setShowDeleteConfirm(false);
  }, [isOpen, mode, provinceId, provinces, usedColors, nextAvailableId]);

  // Validate form
  const validate = useCallback((): string[] => {
    const errs: string[] = [];

    // Check ID
    if (formData.id <= 0) {
      errs.push('Province ID must be greater than 0');
    }
    if (mode === 'create' && usedIds.has(formData.id)) {
      errs.push(`Province ID ${formData.id} is already in use`);
    }

    // Check color
    const colorKey = rgbToKey(formData.color);
    if (usedColors.has(colorKey)) {
      errs.push('This color is already used by another province');
    }

    // Check RGB values
    const { r, g, b } = formData.color;
    if (r < 0 || r > 255 || g < 0 || g > 255 || b < 0 || b > 255) {
      errs.push('RGB values must be between 0 and 255');
    }

    return errs;
  }, [formData, mode, usedIds, usedColors]);

  // Handle save
  const handleSave = useCallback(() => {
    const validationErrors = validate();
    if (validationErrors.length > 0) {
      setErrors(validationErrors);
      return;
    }

    const province: Province = {
      id: formData.id,
      color: formData.color,
      type: formData.type,
      coastal: formData.coastal,
      terrain: formData.terrain,
      continent: formData.continent,
    };

    if (mode === 'create') {
      addProvince(province);
      setSelectedColor(province.color);
    } else {
      updateProvince(province);
    }

    onClose();
  }, [formData, mode, validate, addProvince, updateProvince, setSelectedColor, onClose]);

  // Handle delete
  const handleDelete = useCallback(() => {
    if (provinceId) {
      deleteProvince(provinceId);
      onClose();
    }
  }, [provinceId, deleteProvince, onClose]);

  // Generate new unique color
  const handleGenerateColor = useCallback(() => {
    const newColor = generateUniqueColor(usedColors);
    setFormData(prev => ({ ...prev, color: newColor }));
  }, [usedColors]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-ide-sidebar rounded-lg shadow-xl w-[500px] max-h-[90vh] overflow-hidden border border-ide-border">
        {/* Header */}
        <div className="px-4 py-3 border-b border-ide-border flex items-center justify-between">
          <h2 className="text-lg font-semibold text-ide-text">
            {mode === 'create' ? 'Create New Province' : `Edit Province #${provinceId}`}
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
          {/* Errors */}
          {errors.length > 0 && (
            <div className="bg-red-900/30 border border-red-500/50 rounded p-3">
              <ul className="text-sm text-red-400 space-y-1">
                {errors.map((err, i) => (
                  <li key={i}>• {err}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Province ID */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-ide-text-muted mb-1">
                Province ID
              </label>
              <input
                type="number"
                value={formData.id}
                onChange={(e) => setFormData(prev => ({ 
                  ...prev, 
                  id: parseInt(e.target.value) || 0 
                }))}
                disabled={mode === 'edit'}
                className="w-full px-3 py-2 bg-ide-bg border border-ide-border rounded text-ide-text
                         disabled:opacity-50 disabled:cursor-not-allowed"
              />
              {mode === 'create' && (
                <p className="text-xs text-ide-text-muted mt-1">
                  Next available: {nextAvailableId}
                </p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-ide-text-muted mb-1">
                Continent
              </label>
              <input
                type="number"
                value={formData.continent}
                onChange={(e) => setFormData(prev => ({ 
                  ...prev, 
                  continent: parseInt(e.target.value) || 0 
                }))}
                className="w-full px-3 py-2 bg-ide-bg border border-ide-border rounded text-ide-text"
              />
            </div>
          </div>

          {/* Color */}
          <div>
            <label className="block text-sm font-medium text-ide-text-muted mb-1">
              Province Color
            </label>
            <div className="flex gap-3 items-center">
              <div
                className="w-16 h-16 rounded border-2 border-ide-border"
                style={{ backgroundColor: rgbToHex(formData.color) }}
              />
              <div className="flex-1 grid grid-cols-3 gap-2">
                <div>
                  <label className="block text-xs text-ide-text-muted">R</label>
                  <input
                    type="number"
                    min="0"
                    max="255"
                    value={formData.color.r}
                    onChange={(e) => setFormData(prev => ({
                      ...prev,
                      color: { ...prev.color, r: Math.max(0, Math.min(255, parseInt(e.target.value) || 0)) }
                    }))}
                    className="w-full px-2 py-1 bg-ide-bg border border-ide-border rounded text-ide-text text-center"
                  />
                </div>
                <div>
                  <label className="block text-xs text-ide-text-muted">G</label>
                  <input
                    type="number"
                    min="0"
                    max="255"
                    value={formData.color.g}
                    onChange={(e) => setFormData(prev => ({
                      ...prev,
                      color: { ...prev.color, g: Math.max(0, Math.min(255, parseInt(e.target.value) || 0)) }
                    }))}
                    className="w-full px-2 py-1 bg-ide-bg border border-ide-border rounded text-ide-text text-center"
                  />
                </div>
                <div>
                  <label className="block text-xs text-ide-text-muted">B</label>
                  <input
                    type="number"
                    min="0"
                    max="255"
                    value={formData.color.b}
                    onChange={(e) => setFormData(prev => ({
                      ...prev,
                      color: { ...prev.color, b: Math.max(0, Math.min(255, parseInt(e.target.value) || 0)) }
                    }))}
                    className="w-full px-2 py-1 bg-ide-bg border border-ide-border rounded text-ide-text text-center"
                  />
                </div>
              </div>
              <button
                onClick={handleGenerateColor}
                className="px-3 py-2 bg-ide-hover hover:bg-ide-active rounded text-sm text-ide-text"
                title="Generate random unique color"
              >
                🎲
              </button>
            </div>
            <p className="text-xs text-ide-text-muted mt-1">
              Hex: {rgbToHex(formData.color)}
            </p>
          </div>

          {/* Type */}
          <div>
            <label className="block text-sm font-medium text-ide-text-muted mb-1">
              Province Type
            </label>
            <div className="flex gap-2">
              {PROVINCE_TYPES.map((type) => (
                <button
                  key={type}
                  onClick={() => setFormData(prev => ({ ...prev, type }))}
                  className={`flex-1 px-3 py-2 rounded text-sm font-medium transition-colors ${
                    formData.type === type
                      ? 'bg-blue-600 text-white'
                      : 'bg-ide-hover text-ide-text hover:bg-ide-active'
                  }`}
                >
                  {type === 'land' && '🏞️'} {type === 'sea' && '🌊'} {type === 'lake' && '💧'}
                  {' '}{type.charAt(0).toUpperCase() + type.slice(1)}
                </button>
              ))}
            </div>
          </div>

          {/* Terrain */}
          <div>
            <label className="block text-sm font-medium text-ide-text-muted mb-1">
              Terrain
            </label>
            <select
              value={formData.terrain}
              onChange={(e) => setFormData(prev => ({ 
                ...prev, 
                terrain: e.target.value as TerrainType 
              }))}
              className="w-full px-3 py-2 bg-ide-bg border border-ide-border rounded text-ide-text"
            >
              {TERRAIN_TYPES.map((terrain) => (
                <option key={terrain} value={terrain}>
                  {terrain.charAt(0).toUpperCase() + terrain.slice(1)}
                </option>
              ))}
            </select>
          </div>

          {/* Coastal */}
          <div>
            <label className="flex items-center gap-3 cursor-pointer">
              <input
                type="checkbox"
                checked={formData.coastal}
                onChange={(e) => setFormData(prev => ({ 
                  ...prev, 
                  coastal: e.target.checked 
                }))}
                className="w-4 h-4 accent-blue-500"
              />
              <span className="text-sm text-ide-text">Coastal Province</span>
            </label>
          </div>
        </div>

        {/* Footer */}
        <div className="px-4 py-3 border-t border-ide-border flex items-center justify-between">
          <div>
            {mode === 'edit' && (
              <>
                {showDeleteConfirm ? (
                  <div className="flex items-center gap-2">
                    <span className="text-sm text-red-400">Delete this province?</span>
                    <button
                      onClick={handleDelete}
                      className="px-3 py-1 bg-red-600 hover:bg-red-700 text-white rounded text-sm"
                    >
                      Yes, Delete
                    </button>
                    <button
                      onClick={() => setShowDeleteConfirm(false)}
                      className="px-3 py-1 bg-ide-hover hover:bg-ide-active text-ide-text rounded text-sm"
                    >
                      Cancel
                    </button>
                  </div>
                ) : (
                  <button
                    onClick={() => setShowDeleteConfirm(true)}
                    className="px-3 py-1 text-red-400 hover:text-red-300 text-sm"
                  >
                    Delete Province
                  </button>
                )}
              </>
            )}
          </div>
          <div className="flex gap-2">
            <button
              onClick={onClose}
              className="px-4 py-2 bg-ide-hover hover:bg-ide-active text-ide-text rounded"
            >
              Cancel
            </button>
            <button
              onClick={handleSave}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded"
            >
              {mode === 'create' ? 'Create Province' : 'Save Changes'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProvinceEditorDialog;
