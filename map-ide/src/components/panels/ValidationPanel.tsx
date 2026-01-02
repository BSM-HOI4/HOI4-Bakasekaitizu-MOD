/**
 * Validation Panel
 * 
 * Displays validation results for provinces, states, and strategic regions.
 * Checks for common issues like:
 * - Unassigned provinces
 * - Duplicate province IDs/colors
 * - Empty states
 * - Missing strategic regions
 */

import React, { useMemo, useState, useCallback } from 'react';
import { useProjectStore } from '../../stores/projectStore';
import { useMapStore } from '../../stores/mapStore';
import { ValidationIssue } from '../../types';

interface ValidationPanelProps {
  onSelectProvince?: (id: number) => void;
  onSelectState?: (id: number) => void;
  onSelectRegion?: (id: number) => void;
}

const ValidationPanel: React.FC<ValidationPanelProps> = ({
  onSelectProvince,
  onSelectState,
  onSelectRegion: _onSelectRegion,
}) => {
  const provinces = useProjectStore((state) => state.provinces);
  const states = useProjectStore((state) => state.states);
  const strategicRegions = useProjectStore((state) => state.strategicRegions);
  const aiAreas = useProjectStore((state) => state.aiAreas);
  
  const selectProvince = useMapStore((state) => state.selectProvince);

  const [filter, setFilter] = useState<'all' | 'error' | 'warning'>('all');
  const [expandedCategory, setExpandedCategory] = useState<string | null>('provinces');

  // Run validation checks
  const validationIssues = useMemo((): ValidationIssue[] => {
    const issues: ValidationIssue[] = [];

    // Check provinces
    const colorMap = new Map<string, number[]>();
    let unassignedLandProvinces = 0;
    let unassignedToRegion = 0;

    for (const prov of provinces.values()) {
      // Check for duplicate colors
      const colorKey = `${prov.color.r},${prov.color.g},${prov.color.b}`;
      if (!colorMap.has(colorKey)) {
        colorMap.set(colorKey, []);
      }
      colorMap.get(colorKey)!.push(prov.id);

      // Check land provinces without states
      if (prov.type === 'land' && !prov.stateId) {
        unassignedLandProvinces++;
      }

      // Check provinces without strategic regions
      if (!prov.strategicRegionId) {
        unassignedToRegion++;
      }
    }

    // Report duplicate colors
    for (const [color, ids] of colorMap) {
      if (ids.length > 1) {
        issues.push({
          type: 'error',
          code: 'DUPLICATE_COLOR',
          message: `Duplicate province color ${color}: provinces ${ids.join(', ')}`,
          provinceId: ids[0],
        });
      }
    }

    // Report unassigned provinces summary
    if (unassignedLandProvinces > 0) {
      issues.push({
        type: 'warning',
        code: 'UNASSIGNED_PROVINCES',
        message: `${unassignedLandProvinces} land provinces not assigned to any state`,
      });
    }

    if (unassignedToRegion > 0) {
      issues.push({
        type: 'warning',
        code: 'NO_STRATEGIC_REGION',
        message: `${unassignedToRegion} provinces not assigned to any strategic region`,
      });
    }

    // Check states
    for (const state of states.values()) {
      // Empty states
      if (state.provinces.length === 0) {
        issues.push({
          type: 'error',
          code: 'EMPTY_STATE',
          message: `State #${state.id} "${state.name}" has no provinces`,
          stateId: state.id,
        });
      }

      // States without owner
      if (!state.owner && state.provinces.length > 0) {
        issues.push({
          type: 'warning',
          code: 'NO_OWNER',
          message: `State #${state.id} "${state.name}" has no owner`,
          stateId: state.id,
        });
      }

      // Check for invalid province references
      for (const provId of state.provinces) {
        if (!provinces.has(provId)) {
          issues.push({
            type: 'error',
            code: 'INVALID_PROVINCE_REF',
            message: `State #${state.id} references non-existent province ${provId}`,
            stateId: state.id,
            provinceId: provId,
          });
        }
      }
    }

    // Check strategic regions
    for (const region of strategicRegions.values()) {
      // Empty regions
      if (region.provinces.length === 0) {
        issues.push({
          type: 'warning',
          code: 'EMPTY_REGION',
          message: `Strategic region #${region.id} "${region.name}" has no provinces`,
        });
      }

      // No weather defined
      if (region.weather.length === 0) {
        issues.push({
          type: 'warning',
          code: 'NO_WEATHER',
          message: `Strategic region #${region.id} "${region.name}" has no weather periods`,
        });
      }

      // Check for invalid province references
      for (const provId of region.provinces) {
        if (!provinces.has(provId)) {
          issues.push({
            type: 'error',
            code: 'INVALID_PROVINCE_REF',
            message: `Strategic region #${region.id} references non-existent province ${provId}`,
            provinceId: provId,
          });
        }
      }
    }

    // Check AI areas
    for (const area of aiAreas) {
      // Empty AI areas
      if ((!area.strategicRegions || area.strategicRegions.length === 0) && 
          (!area.continents || area.continents.length === 0)) {
        issues.push({
          type: 'warning',
          code: 'EMPTY_AI_AREA',
          message: `AI area "${area.name}" has no strategic regions or continents`,
        });
      }

      // Check for invalid strategic region references
      if (area.strategicRegions) {
        for (const regionId of area.strategicRegions) {
          if (!strategicRegions.has(regionId)) {
            issues.push({
              type: 'error',
              code: 'INVALID_REGION_REF',
              message: `AI area "${area.name}" references non-existent strategic region ${regionId}`,
            });
          }
        }
      }
    }

    return issues;
  }, [provinces, states, strategicRegions, aiAreas]);

  // Filter issues
  const filteredIssues = useMemo(() => {
    if (filter === 'all') return validationIssues;
    return validationIssues.filter(issue => issue.type === filter);
  }, [validationIssues, filter]);

  // Group issues by category
  const groupedIssues = useMemo(() => {
    const groups: Record<string, ValidationIssue[]> = {
      provinces: [],
      states: [],
      regions: [],
      aiAreas: [],
    };

    for (const issue of filteredIssues) {
      if (issue.code.includes('PROVINCE') || issue.code === 'DUPLICATE_COLOR' || 
          issue.code === 'UNASSIGNED_PROVINCES' || issue.code === 'NO_STRATEGIC_REGION') {
        groups.provinces.push(issue);
      } else if (issue.code.includes('STATE') || issue.code === 'EMPTY_STATE' || 
                 issue.code === 'NO_OWNER') {
        groups.states.push(issue);
      } else if (issue.code.includes('REGION') || issue.code === 'EMPTY_REGION' || 
                 issue.code === 'NO_WEATHER') {
        groups.regions.push(issue);
      } else if (issue.code.includes('AI_AREA')) {
        groups.aiAreas.push(issue);
      }
    }

    return groups;
  }, [filteredIssues]);

  // Handle click on issue
  const handleIssueClick = useCallback((issue: ValidationIssue) => {
    if (issue.provinceId && onSelectProvince) {
      onSelectProvince(issue.provinceId);
      selectProvince(issue.provinceId);
    } else if (issue.stateId && onSelectState) {
      onSelectState(issue.stateId);
    }
  }, [onSelectProvince, onSelectState, selectProvince]);

  // Statistics
  const errorCount = validationIssues.filter(i => i.type === 'error').length;
  const warningCount = validationIssues.filter(i => i.type === 'warning').length;

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="p-3 border-b border-ide-border">
        <h3 className="text-sm font-semibold text-ide-text mb-2">Validation</h3>
        
        {/* Summary */}
        <div className="flex gap-3 mb-2">
          <span className="text-xs text-red-400">
            {errorCount} errors
          </span>
          <span className="text-xs text-yellow-400">
            {warningCount} warnings
          </span>
        </div>

        {/* Filter */}
        <div className="flex gap-1">
          <button
            onClick={() => setFilter('all')}
            className={`px-2 py-1 rounded text-xs ${
              filter === 'all'
                ? 'bg-blue-600 text-white'
                : 'bg-ide-hover text-ide-text hover:bg-ide-active'
            }`}
          >
            All
          </button>
          <button
            onClick={() => setFilter('error')}
            className={`px-2 py-1 rounded text-xs ${
              filter === 'error'
                ? 'bg-red-600 text-white'
                : 'bg-ide-hover text-ide-text hover:bg-ide-active'
            }`}
          >
            Errors
          </button>
          <button
            onClick={() => setFilter('warning')}
            className={`px-2 py-1 rounded text-xs ${
              filter === 'warning'
                ? 'bg-yellow-600 text-white'
                : 'bg-ide-hover text-ide-text hover:bg-ide-active'
            }`}
          >
            Warnings
          </button>
        </div>
      </div>

      {/* Issues List */}
      <div className="flex-1 overflow-y-auto p-2 space-y-2">
        {filteredIssues.length === 0 ? (
          <div className="text-center py-8 text-ide-text-muted text-sm">
            {filter === 'all' 
              ? 'No validation issues found!'
              : `No ${filter}s found`
            }
          </div>
        ) : (
          Object.entries(groupedIssues).map(([category, issues]) => {
            if (issues.length === 0) return null;
            
            const isExpanded = expandedCategory === category;
            const categoryLabels: Record<string, string> = {
              provinces: 'Provinces',
              states: 'States',
              regions: 'Strategic Regions',
              aiAreas: 'AI Areas',
            };

            return (
              <div key={category} className="bg-ide-bg rounded border border-ide-border">
                <button
                  onClick={() => setExpandedCategory(isExpanded ? null : category)}
                  className="w-full px-3 py-2 flex items-center justify-between text-left hover:bg-ide-hover"
                >
                  <span className="text-sm text-ide-text font-medium">
                    {categoryLabels[category]}
                  </span>
                  <span className="text-xs text-ide-text-muted">
                    {issues.length} issues
                    <span className="ml-2">{isExpanded ? '▼' : '▶'}</span>
                  </span>
                </button>
                
                {isExpanded && (
                  <div className="border-t border-ide-border">
                    {issues.map((issue, idx) => (
                      <button
                        key={idx}
                        onClick={() => handleIssueClick(issue)}
                        className="w-full px-3 py-2 text-left hover:bg-ide-hover border-b border-ide-border/50 last:border-b-0"
                      >
                        <div className="flex items-start gap-2">
                          <span className={`text-xs px-1 rounded ${
                            issue.type === 'error'
                              ? 'bg-red-900/50 text-red-400'
                              : 'bg-yellow-900/50 text-yellow-400'
                          }`}>
                            {issue.type === 'error' ? 'ERR' : 'WARN'}
                          </span>
                          <span className="text-xs text-ide-text flex-1">
                            {issue.message}
                          </span>
                        </div>
                        {(issue.provinceId || issue.stateId) && (
                          <div className="text-xs text-ide-text-muted mt-1 ml-8">
                            Click to select
                          </div>
                        )}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>

      {/* Footer */}
      <div className="p-2 border-t border-ide-border">
        <div className="text-xs text-ide-text-muted">
          {provinces.size} provinces • {states.size} states • {strategicRegions.size} regions • {aiAreas.length} AI areas
        </div>
      </div>
    </div>
  );
};

export default ValidationPanel;
