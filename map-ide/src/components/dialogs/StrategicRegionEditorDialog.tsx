/**
 * Strategic Region Editor Dialog
 * 
 * Dialog for editing strategic region properties, weather settings,
 * and province assignments.
 */

import React, { useState, useEffect, useMemo, useCallback } from 'react';
import { useProjectStore } from '../../stores/projectStore';
import { useMapStore } from '../../stores/mapStore';
import { StrategicRegion, Province, WeatherPeriod } from '../../types';

interface StrategicRegionEditorDialogProps {
  isOpen: boolean;
  onClose: () => void;
  regionId: number;
}

const DEFAULT_WEATHER_PERIOD: WeatherPeriod = {
  between: [0, 30],
  temperature: [-5, 20],
  no_phenomenon: 0.5,
  rain_light: 0.2,
  rain_heavy: 0.1,
  snow: 0.1,
  blizzard: 0.05,
  arctic_water: 0,
  mud: 0.05,
  sandstorm: 0,
  min_snow_level: 0,
};

const StrategicRegionEditorDialog: React.FC<StrategicRegionEditorDialogProps> = ({
  isOpen,
  onClose,
  regionId,
}) => {
  const strategicRegions = useProjectStore((state) => state.strategicRegions);
  const provinces = useProjectStore((state) => state.provinces);
  const updateStrategicRegion = useProjectStore((state) => state.updateStrategicRegion);
  const saveStrategicRegion = useProjectStore((state) => state.saveStrategicRegion);
  const addProvinceToRegion = useProjectStore((state) => state.addProvinceToRegion);
  const removeProvinceFromRegion = useProjectStore((state) => state.removeProvinceFromRegion);
  
  const selectedProvinceId = useMapStore((state) => state.selectedProvinceId);

  const regionData = strategicRegions.get(regionId);

  // Form state
  const [formData, setFormData] = useState<{
    name: string;
    weather: WeatherPeriod[];
  }>({
    name: '',
    weather: [],
  });

  const [selectedPeriodIndex, setSelectedPeriodIndex] = useState<number>(0);
  const [isSaving, setIsSaving] = useState(false);
  const [saveMessage, setSaveMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  // Initialize form data
  useEffect(() => {
    if (!isOpen || !regionData) return;

    setFormData({
      name: regionData.name,
      weather: regionData.weather.map(w => ({ ...w })),
    });
    setSelectedPeriodIndex(0);
    setSaveMessage(null);
  }, [isOpen, regionData]);

  // Get assigned provinces
  const assignedProvinces = useMemo(() => {
    if (!regionData) return [];
    return regionData.provinces
      .map(id => provinces.get(id))
      .filter((p): p is Province => p !== undefined);
  }, [regionData, provinces]);

  // Get unassigned provinces
  const unassignedProvinces = useMemo(() => {
    return Array.from(provinces.values())
      .filter(p => !p.strategicRegionId)
      .sort((a, b) => a.id - b.id);
  }, [provinces]);

  // Handle save
  const handleSave = useCallback(async () => {
    if (!regionData) return;

    setIsSaving(true);
    setSaveMessage(null);

    const updatedRegion: StrategicRegion = {
      ...regionData,
      name: formData.name,
      weather: formData.weather,
    };

    updateStrategicRegion(updatedRegion);
    
    const success = await saveStrategicRegion(regionId);
    
    setIsSaving(false);
    setSaveMessage({
      type: success ? 'success' : 'error',
      text: success ? 'Strategic region saved successfully!' : 'Failed to save strategic region file',
    });
  }, [regionData, formData, regionId, updateStrategicRegion, saveStrategicRegion]);

  // Handle add weather period
  const handleAddWeatherPeriod = useCallback(() => {
    setFormData(prev => ({
      ...prev,
      weather: [...prev.weather, { ...DEFAULT_WEATHER_PERIOD }],
    }));
    setSelectedPeriodIndex(formData.weather.length);
  }, [formData.weather.length]);

  // Handle remove weather period
  const handleRemoveWeatherPeriod = useCallback((index: number) => {
    setFormData(prev => ({
      ...prev,
      weather: prev.weather.filter((_, i) => i !== index),
    }));
    if (selectedPeriodIndex >= index && selectedPeriodIndex > 0) {
      setSelectedPeriodIndex(selectedPeriodIndex - 1);
    }
  }, [selectedPeriodIndex]);

  // Handle update weather period
  const updateWeatherPeriod = useCallback((index: number, updates: Partial<WeatherPeriod>) => {
    setFormData(prev => ({
      ...prev,
      weather: prev.weather.map((w, i) => 
        i === index ? { ...w, ...updates } : w
      ),
    }));
  }, []);

  // Handle add province
  const handleAddProvince = useCallback((provinceId: number) => {
    addProvinceToRegion(regionId, provinceId);
  }, [regionId, addProvinceToRegion]);

  // Handle remove province
  const handleRemoveProvince = useCallback((provinceId: number) => {
    removeProvinceFromRegion(regionId, provinceId);
  }, [regionId, removeProvinceFromRegion]);

  // Handle add selected province
  const handleAddSelectedProvince = useCallback(() => {
    if (selectedProvinceId) {
      const prov = provinces.get(selectedProvinceId);
      if (prov && !prov.strategicRegionId) {
        handleAddProvince(selectedProvinceId);
      }
    }
  }, [selectedProvinceId, provinces, handleAddProvince]);

  if (!isOpen || !regionData) return null;

  const currentPeriod = formData.weather[selectedPeriodIndex];

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-ide-sidebar rounded-lg shadow-xl w-[800px] max-h-[90vh] overflow-hidden border border-ide-border">
        {/* Header */}
        <div className="px-4 py-3 border-b border-ide-border flex items-center justify-between">
          <h2 className="text-lg font-semibold text-ide-text">
            Edit Strategic Region #{regionId}
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

          {/* Basic Info */}
          <div>
            <label className="block text-sm font-medium text-ide-text-muted mb-1">
              Region Name (Localisation Key)
            </label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
              className="w-full px-3 py-2 bg-ide-bg border border-ide-border rounded text-ide-text"
            />
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
                    provinces.get(selectedProvinceId)?.strategicRegionId !== undefined
                  }
                  className="px-2 py-1 bg-cyan-600 hover:bg-cyan-700 disabled:bg-gray-600 
                           disabled:cursor-not-allowed text-white rounded text-xs"
                >
                  Add Selected (#{selectedProvinceId})
                </button>
              )}
            </div>
            <div className="bg-ide-bg rounded border border-ide-border p-2 max-h-28 overflow-y-auto">
              <div className="flex flex-wrap gap-1">
                {assignedProvinces.map(prov => (
                  <span
                    key={prov.id}
                    className={`px-2 py-0.5 rounded text-xs flex items-center gap-1 ${
                      prov.type === 'land' 
                        ? 'bg-green-900/30 text-green-400' 
                        : prov.type === 'sea'
                        ? 'bg-blue-900/30 text-blue-400'
                        : 'bg-cyan-900/30 text-cyan-400'
                    }`}
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

          {/* Weather Periods */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <label className="block text-sm font-medium text-ide-text-muted">
                Weather Periods ({formData.weather.length})
              </label>
              <button
                onClick={handleAddWeatherPeriod}
                className="px-2 py-1 bg-blue-600 hover:bg-blue-700 text-white rounded text-xs"
              >
                + Add Period
              </button>
            </div>

            {formData.weather.length > 0 && (
              <div className="space-y-3">
                {/* Period tabs */}
                <div className="flex gap-1 flex-wrap">
                  {formData.weather.map((period, idx) => (
                    <button
                      key={idx}
                      onClick={() => setSelectedPeriodIndex(idx)}
                      className={`px-3 py-1 rounded text-xs ${
                        selectedPeriodIndex === idx
                          ? 'bg-blue-600 text-white'
                          : 'bg-ide-hover text-ide-text hover:bg-ide-active'
                      }`}
                    >
                      Day {period.between[0]}-{period.between[1]}
                    </button>
                  ))}
                </div>

                {/* Period editor */}
                {currentPeriod && (
                  <div className="bg-ide-bg rounded border border-ide-border p-3 space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-ide-text font-medium">
                        Period {selectedPeriodIndex + 1}
                      </span>
                      <button
                        onClick={() => handleRemoveWeatherPeriod(selectedPeriodIndex)}
                        className="px-2 py-0.5 text-red-400 hover:text-red-300 text-xs"
                      >
                        Remove
                      </button>
                    </div>

                    {/* Date Range */}
                    <div className="grid grid-cols-2 gap-3">
                      <div>
                        <label className="block text-xs text-ide-text-muted mb-1">
                          Start Day
                        </label>
                        <input
                          type="number"
                          min="0"
                          max="30"
                          value={currentPeriod.between[0]}
                          onChange={(e) => updateWeatherPeriod(selectedPeriodIndex, {
                            between: [parseInt(e.target.value) || 0, currentPeriod.between[1]]
                          })}
                          className="w-full px-2 py-1 bg-ide-sidebar border border-ide-border rounded text-ide-text text-sm"
                        />
                      </div>
                      <div>
                        <label className="block text-xs text-ide-text-muted mb-1">
                          End Day
                        </label>
                        <input
                          type="number"
                          min="0"
                          max="30"
                          value={currentPeriod.between[1]}
                          onChange={(e) => updateWeatherPeriod(selectedPeriodIndex, {
                            between: [currentPeriod.between[0], parseInt(e.target.value) || 30]
                          })}
                          className="w-full px-2 py-1 bg-ide-sidebar border border-ide-border rounded text-ide-text text-sm"
                        />
                      </div>
                    </div>

                    {/* Temperature Range */}
                    <div className="grid grid-cols-2 gap-3">
                      <div>
                        <label className="block text-xs text-ide-text-muted mb-1">
                          Min Temp (°C)
                        </label>
                        <input
                          type="number"
                          value={currentPeriod.temperature[0]}
                          onChange={(e) => updateWeatherPeriod(selectedPeriodIndex, {
                            temperature: [parseInt(e.target.value) || 0, currentPeriod.temperature[1]]
                          })}
                          className="w-full px-2 py-1 bg-ide-sidebar border border-ide-border rounded text-ide-text text-sm"
                        />
                      </div>
                      <div>
                        <label className="block text-xs text-ide-text-muted mb-1">
                          Max Temp (°C)
                        </label>
                        <input
                          type="number"
                          value={currentPeriod.temperature[1]}
                          onChange={(e) => updateWeatherPeriod(selectedPeriodIndex, {
                            temperature: [currentPeriod.temperature[0], parseInt(e.target.value) || 20]
                          })}
                          className="w-full px-2 py-1 bg-ide-sidebar border border-ide-border rounded text-ide-text text-sm"
                        />
                      </div>
                    </div>

                    {/* Weather Probabilities */}
                    <div className="grid grid-cols-3 gap-2">
                      {[
                        { key: 'no_phenomenon', label: 'Clear' },
                        { key: 'rain_light', label: 'Light Rain' },
                        { key: 'rain_heavy', label: 'Heavy Rain' },
                        { key: 'snow', label: 'Snow' },
                        { key: 'blizzard', label: 'Blizzard' },
                        { key: 'arctic_water', label: 'Arctic Water' },
                        { key: 'mud', label: 'Mud' },
                        { key: 'sandstorm', label: 'Sandstorm' },
                        { key: 'min_snow_level', label: 'Min Snow Lvl' },
                      ].map(({ key, label }) => (
                        <div key={key}>
                          <label className="block text-xs text-ide-text-muted mb-1">
                            {label}
                          </label>
                          <input
                            type="number"
                            step="0.01"
                            min="0"
                            max={key === 'min_snow_level' ? '1' : '1'}
                            value={(currentPeriod as unknown as Record<string, number>)[key]}
                            onChange={(e) => updateWeatherPeriod(selectedPeriodIndex, {
                              [key]: parseFloat(e.target.value) || 0
                            })}
                            className="w-full px-2 py-1 bg-ide-sidebar border border-ide-border rounded text-ide-text text-sm"
                          />
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {formData.weather.length === 0 && (
              <div className="bg-ide-bg rounded border border-ide-border p-3 text-center text-ide-text-muted text-sm">
                No weather periods defined. Click "Add Period" to create one.
              </div>
            )}
          </div>

          {/* Unassigned Provinces */}
          {unassignedProvinces.length > 0 && (
            <div>
              <label className="block text-sm font-medium text-ide-text-muted mb-2">
                Unassigned Provinces ({unassignedProvinces.length})
              </label>
              <div className="bg-ide-bg rounded border border-ide-border p-2 max-h-24 overflow-y-auto">
                <div className="flex flex-wrap gap-1">
                  {unassignedProvinces.slice(0, 50).map(prov => (
                    <button
                      key={prov.id}
                      onClick={() => handleAddProvince(prov.id)}
                      className={`px-2 py-0.5 rounded text-xs hover:opacity-80 ${
                        prov.type === 'land' 
                          ? 'bg-yellow-900/30 border border-yellow-600/30 text-yellow-400' 
                          : prov.type === 'sea'
                          ? 'bg-blue-900/30 border border-blue-600/30 text-blue-400'
                          : 'bg-cyan-900/30 border border-cyan-600/30 text-cyan-400'
                      }`}
                    >
                      +{prov.id}
                    </button>
                  ))}
                  {unassignedProvinces.length > 50 && (
                    <span className="text-ide-text-muted text-xs">
                      ...and {unassignedProvinces.length - 50} more
                    </span>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="px-4 py-3 border-t border-ide-border flex items-center justify-between">
          <div className="text-xs text-ide-text-muted">
            {regionData.filePath && `File: ${regionData.filePath.split('/').pop()}`}
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
              className="px-4 py-2 bg-cyan-600 hover:bg-cyan-700 disabled:bg-cyan-800 
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

export default StrategicRegionEditorDialog;
