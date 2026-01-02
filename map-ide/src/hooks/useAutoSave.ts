/**
 * Auto-Save Hook
 * 
 * Provides automatic saving functionality with configurable intervals.
 * Creates backup files before saving.
 */

import { useEffect, useRef, useCallback, useState } from 'react';
import { useProjectStore } from '../stores/projectStore';
import { useMapStore } from '../stores/mapStore';

interface AutoSaveOptions {
  enabled: boolean;
  intervalMs: number;
  createBackup: boolean;
}

interface AutoSaveState {
  lastSave: Date | null;
  isSaving: boolean;
  error: string | null;
  pendingChanges: boolean;
}

export function useAutoSave(options: AutoSaveOptions = {
  enabled: true,
  intervalMs: 60000, // 1 minute
  createBackup: true,
}) {
  const project = useProjectStore((state) => state.project);
  const isDirty = useProjectStore((state) => state.isDirty);
  const markClean = useProjectStore((state) => state.markClean);
  const saveDefinitionCSV = useProjectStore((state) => state.saveDefinitionCSV);
  const saveAllStates = useProjectStore((state) => state.saveAllStates);
  const saveAllStrategicRegions = useProjectStore((state) => state.saveAllStrategicRegions);
  const saveAIAreas = useProjectStore((state) => state.saveAIAreas);
  
  const bmpEditor = useMapStore((state) => state.bmpEditor);
  const saveBMP = useMapStore((state) => state.saveBMP);

  const [state, setState] = useState<AutoSaveState>({
    lastSave: null,
    isSaving: false,
    error: null,
    pendingChanges: false,
  });

  const saveIntervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  // Create backup of a file
  const createBackup = useCallback(async (filePath: string) => {
    if (!options.createBackup) return;
    
    try {
      // Create backup in same directory with timestamp
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
      const backupPath = `${filePath}.${timestamp}.bak`;
      
      // Read original file
      const result = await window.electronAPI.readTextFile(filePath);
      if (result.success && result.data) {
        // Write backup
        await window.electronAPI.writeTextFile(backupPath, result.data);
      }
    } catch (err) {
      console.warn('Failed to create backup:', err);
    }
  }, [options.createBackup]);

  // Perform save operation
  const performSave = useCallback(async () => {
    if (!project || state.isSaving) return;
    
    // Check if there are any changes to save
    if (!isDirty && !bmpEditor?.isDirty) {
      return;
    }

    setState(prev => ({ ...prev, isSaving: true, error: null }));
    
    try {
      const errors: string[] = [];

      // Save provinces.bmp if dirty
      if (bmpEditor?.isDirty) {
        try {
          // Create backup first
          await createBackup(`${project.mapPath}/provinces.bmp`);
          
          const bmpData = saveBMP();
          if (bmpData) {
            const result = await window.electronAPI.writeFile(
              `${project.mapPath}/provinces.bmp`,
              bmpData
            );
            if (!result.success) {
              errors.push('Failed to save provinces.bmp');
            }
          }
        } catch (err) {
          errors.push('Error saving provinces.bmp');
        }
      }

      // Save definition.csv
      if (isDirty) {
        try {
          await createBackup(`${project.mapPath}/definition.csv`);
          const success = await saveDefinitionCSV();
          if (!success) {
            errors.push('Failed to save definition.csv');
          }
        } catch (err) {
          errors.push('Error saving definition.csv');
        }
      }

      // Save states
      try {
        const success = await saveAllStates();
        if (!success) {
          errors.push('Some state files failed to save');
        }
      } catch (err) {
        errors.push('Error saving state files');
      }

      // Save strategic regions
      try {
        const success = await saveAllStrategicRegions();
        if (!success) {
          errors.push('Some strategic region files failed to save');
        }
      } catch (err) {
        errors.push('Error saving strategic region files');
      }

      // Save AI areas
      try {
        const success = await saveAIAreas();
        if (!success) {
          errors.push('Failed to save AI areas');
        }
      } catch (err) {
        errors.push('Error saving AI areas');
      }

      if (errors.length === 0) {
        markClean();
        setState(prev => ({
          ...prev,
          isSaving: false,
          lastSave: new Date(),
          pendingChanges: false,
        }));
      } else {
        setState(prev => ({
          ...prev,
          isSaving: false,
          error: errors.join('; '),
        }));
      }
    } catch (err) {
      setState(prev => ({
        ...prev,
        isSaving: false,
        error: err instanceof Error ? err.message : 'Save failed',
      }));
    }
  }, [
    project, state.isSaving, isDirty, bmpEditor,
    createBackup, saveBMP, saveDefinitionCSV, saveAllStates,
    saveAllStrategicRegions, saveAIAreas, markClean
  ]);

  // Setup auto-save interval
  useEffect(() => {
    if (!options.enabled || !project) {
      if (saveIntervalRef.current) {
        clearInterval(saveIntervalRef.current);
        saveIntervalRef.current = null;
      }
      return;
    }

    saveIntervalRef.current = setInterval(() => {
      if (isDirty || bmpEditor?.isDirty) {
        performSave();
      }
    }, options.intervalMs);

    return () => {
      if (saveIntervalRef.current) {
        clearInterval(saveIntervalRef.current);
      }
    };
  }, [options.enabled, options.intervalMs, project, isDirty, bmpEditor, performSave]);

  // Track pending changes
  useEffect(() => {
    setState(prev => ({
      ...prev,
      pendingChanges: isDirty || Boolean(bmpEditor?.isDirty),
    }));
  }, [isDirty, bmpEditor]);

  // Manual save trigger
  const saveNow = useCallback(async () => {
    await performSave();
  }, [performSave]);

  return {
    ...state,
    saveNow,
    isEnabled: options.enabled,
  };
}

export default useAutoSave;
