/**
 * Country Colors Panel
 * 
 * Manages country colors from common/countries/colors.txt
 * Allows viewing and editing country colors.
 */

import React, { useState, useEffect, useMemo, useCallback } from 'react';
import { useProjectStore } from '../../stores/projectStore';
import { CountryColor, RGB } from '../../types';
import { rgbToHex } from '../../utils/colorUtils';

const CountryColorsPanel: React.FC = () => {
  const project = useProjectStore((state) => state.project);
  
  const [colors, setColors] = useState<CountryColor[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [editingTag, setEditingTag] = useState<string | null>(null);
  const [editColor, setEditColor] = useState<RGB>({ r: 0, g: 0, b: 0 });
  const [isSaving, setIsSaving] = useState(false);

  // Load colors from file
  useEffect(() => {
    const loadColors = async () => {
      if (!project) return;
      
      setIsLoading(true);
      setError(null);
      
      try {
        const colorsPath = `${project.commonPath}/countries/colors.txt`;
        const result = await window.electronAPI.readTextFile(colorsPath);
        
        if (result.success && result.data) {
          const parsed = parseCountryColors(result.data);
          setColors(parsed);
        } else {
          // Try alternate paths
          const altPath = `${project.commonPath}/country_colors.txt`;
          const altResult = await window.electronAPI.readTextFile(altPath);
          
          if (altResult.success && altResult.data) {
            const parsed = parseCountryColors(altResult.data);
            setColors(parsed);
          } else {
            setError('No country colors file found');
          }
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load country colors');
      }
      
      setIsLoading(false);
    };
    
    loadColors();
  }, [project]);

  // Filter colors
  const filteredColors = useMemo(() => {
    if (!searchTerm.trim()) return colors;
    const term = searchTerm.toLowerCase();
    return colors.filter(c => c.tag.toLowerCase().includes(term));
  }, [colors, searchTerm]);

  // Parse country colors from text
  const parseCountryColors = (content: string): CountryColor[] => {
    const result: CountryColor[] = [];
    const lines = content.split('\n');
    
    let currentTag = '';
    let inBlock = false;
    let bracketCount = 0;
    let colorData: { color?: RGB; colorUI?: RGB } = {};
    
    for (const line of lines) {
      const trimmed = line.trim();
      
      // Skip comments and empty lines
      if (trimmed.startsWith('#') || trimmed === '') continue;
      
      // Match country tag start
      const tagMatch = trimmed.match(/^([A-Z]{3})\s*=\s*{/);
      if (tagMatch) {
        currentTag = tagMatch[1];
        inBlock = true;
        bracketCount = 1;
        colorData = {};
        continue;
      }
      
      if (inBlock) {
        // Count brackets
        bracketCount += (trimmed.match(/{/g) || []).length;
        bracketCount -= (trimmed.match(/}/g) || []).length;
        
        // Parse color
        const colorMatch = trimmed.match(/color\s*=\s*(?:rgb\s*)?\{\s*(\d+)\s+(\d+)\s+(\d+)\s*\}/i);
        if (colorMatch) {
          colorData.color = {
            r: parseInt(colorMatch[1]),
            g: parseInt(colorMatch[2]),
            b: parseInt(colorMatch[3]),
          };
        }
        
        // Parse color_ui
        const colorUIMatch = trimmed.match(/color_ui\s*=\s*(?:rgb\s*)?\{\s*(\d+)\s+(\d+)\s+(\d+)\s*\}/i);
        if (colorUIMatch) {
          colorData.colorUI = {
            r: parseInt(colorUIMatch[1]),
            g: parseInt(colorUIMatch[2]),
            b: parseInt(colorUIMatch[3]),
          };
        }
        
        // End of block
        if (bracketCount === 0) {
          if (currentTag && colorData.color) {
            result.push({
              tag: currentTag,
              color: { type: 'rgb', value: colorData.color },
              colorUI: colorData.colorUI 
                ? { type: 'rgb', value: colorData.colorUI }
                : { type: 'rgb', value: colorData.color },
            });
          }
          inBlock = false;
          currentTag = '';
        }
      }
    }
    
    return result.sort((a, b) => a.tag.localeCompare(b.tag));
  };

  // Handle edit start
  const handleEditStart = useCallback((country: CountryColor) => {
    setEditingTag(country.tag);
    setEditColor(country.color.value as RGB);
  }, []);

  // Handle edit cancel
  const handleEditCancel = useCallback(() => {
    setEditingTag(null);
  }, []);

  // Handle save
  const handleSave = useCallback(async () => {
    if (!editingTag || !project) return;
    
    setIsSaving(true);
    
    // Update color in state
    setColors(prev => prev.map(c => 
      c.tag === editingTag
        ? { ...c, color: { type: 'rgb' as const, value: editColor } }
        : c
    ));
    
    // Generate and save file
    const content = serializeCountryColors(colors.map(c =>
      c.tag === editingTag
        ? { ...c, color: { type: 'rgb' as const, value: editColor } }
        : c
    ));
    
    try {
      const colorsPath = `${project.commonPath}/countries/colors.txt`;
      await window.electronAPI.writeTextFile(colorsPath, content);
    } catch (err) {
      console.error('Failed to save country colors:', err);
    }
    
    setIsSaving(false);
    setEditingTag(null);
  }, [editingTag, editColor, project, colors]);

  // Serialize colors to text
  const serializeCountryColors = (colors: CountryColor[]): string => {
    return colors.map(c => {
      const rgb = c.color.value as RGB;
      const rgbUI = c.colorUI.value as RGB;
      return `${c.tag} = {\n\tcolor = rgb { ${rgb.r} ${rgb.g} ${rgb.b} }\n\tcolor_ui = rgb { ${rgbUI.r} ${rgbUI.g} ${rgbUI.b} }\n}`;
    }).join('\n\n');
  };

  if (isLoading) {
    return (
      <div className="h-full flex items-center justify-center text-ide-text-muted">
        Loading country colors...
      </div>
    );
  }

  if (error) {
    return (
      <div className="h-full flex flex-col items-center justify-center p-4 text-center">
        <div className="text-red-400 mb-2">{error}</div>
        <div className="text-xs text-ide-text-muted">
          Country colors file not found at common/countries/colors.txt
        </div>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="p-3 border-b border-ide-border">
        <h3 className="text-sm font-semibold text-ide-text mb-2">Country Colors</h3>
        <input
          type="text"
          placeholder="Search by country tag..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value.toUpperCase())}
          className="w-full px-3 py-2 bg-ide-bg border border-ide-border rounded text-ide-text text-sm"
        />
        <div className="text-xs text-ide-text-muted mt-1">
          {filteredColors.length} countries
        </div>
      </div>

      {/* Colors List */}
      <div className="flex-1 overflow-y-auto">
        {filteredColors.length === 0 ? (
          <div className="p-4 text-center text-ide-text-muted text-sm">
            {searchTerm ? 'No countries found' : 'No country colors loaded'}
          </div>
        ) : (
          <div className="divide-y divide-ide-border/50">
            {filteredColors.map((country) => {
              const rgb = country.color.value as RGB;
              const isEditing = editingTag === country.tag;
              
              return (
                <div
                  key={country.tag}
                  className="px-3 py-2 hover:bg-ide-hover"
                >
                  {isEditing ? (
                    <div className="space-y-2">
                      <div className="flex items-center gap-2">
                        <span className="text-sm font-mono text-ide-text">{country.tag}</span>
                        <div
                          className="w-6 h-6 rounded border border-ide-border"
                          style={{ backgroundColor: rgbToHex(editColor) }}
                        />
                      </div>
                      <div className="grid grid-cols-3 gap-2">
                        <div>
                          <label className="block text-xs text-ide-text-muted">R</label>
                          <input
                            type="number"
                            min="0"
                            max="255"
                            value={editColor.r}
                            onChange={(e) => setEditColor(prev => ({
                              ...prev,
                              r: Math.max(0, Math.min(255, parseInt(e.target.value) || 0))
                            }))}
                            className="w-full px-2 py-1 bg-ide-bg border border-ide-border rounded text-ide-text text-sm"
                          />
                        </div>
                        <div>
                          <label className="block text-xs text-ide-text-muted">G</label>
                          <input
                            type="number"
                            min="0"
                            max="255"
                            value={editColor.g}
                            onChange={(e) => setEditColor(prev => ({
                              ...prev,
                              g: Math.max(0, Math.min(255, parseInt(e.target.value) || 0))
                            }))}
                            className="w-full px-2 py-1 bg-ide-bg border border-ide-border rounded text-ide-text text-sm"
                          />
                        </div>
                        <div>
                          <label className="block text-xs text-ide-text-muted">B</label>
                          <input
                            type="number"
                            min="0"
                            max="255"
                            value={editColor.b}
                            onChange={(e) => setEditColor(prev => ({
                              ...prev,
                              b: Math.max(0, Math.min(255, parseInt(e.target.value) || 0))
                            }))}
                            className="w-full px-2 py-1 bg-ide-bg border border-ide-border rounded text-ide-text text-sm"
                          />
                        </div>
                      </div>
                      <div className="flex justify-end gap-2">
                        <button
                          onClick={handleEditCancel}
                          className="px-2 py-1 text-xs bg-ide-hover hover:bg-ide-active text-ide-text rounded"
                        >
                          Cancel
                        </button>
                        <button
                          onClick={handleSave}
                          disabled={isSaving}
                          className="px-2 py-1 text-xs bg-blue-600 hover:bg-blue-700 text-white rounded"
                        >
                          {isSaving ? 'Saving...' : 'Save'}
                        </button>
                      </div>
                    </div>
                  ) : (
                    <button
                      onClick={() => handleEditStart(country)}
                      className="w-full flex items-center gap-3 text-left"
                    >
                      <div
                        className="w-8 h-8 rounded border border-ide-border flex-shrink-0"
                        style={{ backgroundColor: rgbToHex(rgb) }}
                      />
                      <div>
                        <span className="text-sm font-mono text-ide-text">{country.tag}</span>
                        <div className="text-xs text-ide-text-muted">
                          RGB({rgb.r}, {rgb.g}, {rgb.b}) • {rgbToHex(rgb)}
                        </div>
                      </div>
                    </button>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};

export default CountryColorsPanel;
