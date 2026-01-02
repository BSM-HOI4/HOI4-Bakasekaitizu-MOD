import React, { useCallback, useEffect, useState } from 'react';
import { useProjectStore } from './stores/projectStore';
import { useMapStore } from './stores/mapStore';
import Header from './components/layout/Header';
import Sidebar from './components/layout/Sidebar';
import StatusBar from './components/layout/StatusBar';
import WebGLMapCanvas from './components/map/WebGLMapCanvas';
import PropertyPanel from './components/panels/PropertyPanel';
import LayerPanel from './components/panels/LayerPanel';
import ValidationPanel from './components/panels/ValidationPanel';
import SearchPanel from './components/panels/SearchPanel';
import CountryColorsPanel from './components/panels/CountryColorsPanel';
import WelcomeScreen from './components/WelcomeScreen';
import ProvinceEditorDialog from './components/dialogs/ProvinceEditorDialog';
import StateEditorDialog from './components/dialogs/StateEditorDialog';
import StrategicRegionEditorDialog from './components/dialogs/StrategicRegionEditorDialog';
import AIAreaEditorDialog from './components/dialogs/AIAreaEditorDialog';
import { useAutoSave } from './hooks/useAutoSave';

type RightPanelTab = 'properties' | 'layers' | 'validation' | 'search' | 'countries';

const App: React.FC = () => {
  const project = useProjectStore((state) => state.project);
  const openProject = useProjectStore((state) => state.openProject);
  const isLoading = useProjectStore((state) => state.isLoading);
  // isDirty is tracked by useAutoSave hook
  const loadBMP = useMapStore((state) => state.loadBMP);
  
  // Right panel tab state
  const [rightPanelTab, setRightPanelTab] = useState<RightPanelTab>('layers');
  
  // Dialog states
  const [provinceDialog, setProvinceDialog] = useState<{
    isOpen: boolean;
    mode: 'create' | 'edit';
    provinceId?: number;
  }>({ isOpen: false, mode: 'create' });
  
  const [stateDialog, setStateDialog] = useState<{
    isOpen: boolean;
    stateId: number;
  }>({ isOpen: false, stateId: 0 });
  
  const [regionDialog, setRegionDialog] = useState<{
    isOpen: boolean;
    regionId: number;
  }>({ isOpen: false, regionId: 0 });
  
  const [aiAreaDialog, setAIAreaDialog] = useState<{
    isOpen: boolean;
    areaName: string;
  }>({ isOpen: false, areaName: '' });

  // Auto-save settings
  const [autoSaveEnabled, setAutoSaveEnabled] = useState(true);
  const { lastSave, isSaving, error: saveError, saveNow, pendingChanges } = useAutoSave({
    enabled: autoSaveEnabled,
    intervalMs: 120000, // 2 minutes
    createBackup: true,
  });

  // Handle opening a project
  const handleOpenProject = useCallback(async () => {
    const folderPath = await window.electronAPI.openFolder();
    if (folderPath) {
      await openProject(folderPath);
    }
  }, [openProject]);

  // Load BMP when project is loaded
  useEffect(() => {
    const loadMapBMP = async () => {
      if (!project) return;

      // Check if electronAPI is available
      if (typeof window.electronAPI === 'undefined') {
        console.warn('ElectronAPI not available, generating test map');
        // Generate a test BMP for browser debugging
        const testBMP = generateTestBMP(512, 512);
        loadBMP(testBMP);
        return;
      }

      const bmpPath = `${project.mapPath}/provinces.bmp`;
      console.log('Loading BMP from:', bmpPath);
      const result = await window.electronAPI.readFile(bmpPath);
      
      if (result.success && result.data) {
        console.log('BMP loaded successfully, size:', result.data.byteLength);
        loadBMP(result.data);
      } else {
        console.error('Failed to load BMP:', result.error);
      }
    };

    loadMapBMP();
  }, [project, loadBMP]);

  // Generate test BMP for browser debugging
  function generateTestBMP(width: number, height: number): ArrayBuffer {
    const rowPadding = (4 - ((width * 3) % 4)) % 4;
    const paddedRowSize = width * 3 + rowPadding;
    const imageSize = paddedRowSize * height;
    const fileSize = 54 + imageSize;

    const buffer = new ArrayBuffer(fileSize);
    const view = new DataView(buffer);
    const data = new Uint8Array(buffer);

    // BMP header
    view.setUint8(0, 0x42); // 'B'
    view.setUint8(1, 0x4D); // 'M'
    view.setUint32(2, fileSize, true);
    view.setUint32(10, 54, true);
    view.setUint32(14, 40, true);
    view.setInt32(18, width, true);
    view.setInt32(22, height, true);
    view.setUint16(26, 1, true);
    view.setUint16(28, 24, true);
    view.setUint32(30, 0, true);
    view.setUint32(34, imageSize, true);

    // Generate colorful province-like data
    for (let y = 0; y < height; y++) {
      const srcY = height - 1 - y;
      const dstOffset = 54 + y * paddedRowSize;

      for (let x = 0; x < width; x++) {
        const dstIdx = dstOffset + x * 3;
        // Create a grid of different colored "provinces"
        const gridX = Math.floor(x / 32);
        const gridY = Math.floor(srcY / 32);
        const seed = (gridX * 17 + gridY * 31) % 256;
        
        // BGR order
        data[dstIdx] = (seed * 3 + 50) % 256;     // B
        data[dstIdx + 1] = (seed * 7 + 100) % 256; // G
        data[dstIdx + 2] = (seed * 11 + 150) % 256; // R
      }
    }

    return buffer;
  }

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Ctrl/Cmd + O: Open project
      if ((e.ctrlKey || e.metaKey) && e.key === 'o') {
        e.preventDefault();
        handleOpenProject();
      }

      // Ctrl/Cmd + S: Save
      if ((e.ctrlKey || e.metaKey) && e.key === 's') {
        e.preventDefault();
        saveNow();
      }

      // Ctrl/Cmd + Z: Undo
      if ((e.ctrlKey || e.metaKey) && e.key === 'z' && !e.shiftKey) {
        e.preventDefault();
        useMapStore.getState().undo();
      }

      // Ctrl/Cmd + Shift + Z or Ctrl + Y: Redo
      if (
        ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'z') ||
        ((e.ctrlKey || e.metaKey) && e.key === 'y')
      ) {
        e.preventDefault();
        useMapStore.getState().redo();
      }

      // Ctrl/Cmd + F: Focus search
      if ((e.ctrlKey || e.metaKey) && e.key === 'f') {
        e.preventDefault();
        setRightPanelTab('search');
      }

      // Ctrl/Cmd + N: New province
      if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
        e.preventDefault();
        setProvinceDialog({ isOpen: true, mode: 'create' });
      }

      // + / = : Zoom in
      if (e.key === '+' || e.key === '=') {
        useMapStore.getState().zoomIn();
      }

      // - : Zoom out
      if (e.key === '-') {
        useMapStore.getState().zoomOut();
      }

      // Tool shortcuts
      if (!e.ctrlKey && !e.metaKey && !e.altKey) {
        switch (e.key) {
          case 'v':
            useMapStore.getState().setActiveTool('select');
            break;
          case 'b':
            useMapStore.getState().setActiveTool('brush');
            break;
          case 'g':
            useMapStore.getState().setActiveTool('fill');
            break;
          case 'p':
            useMapStore.getState().setActiveTool('pencil');
            break;
          case 'i':
            useMapStore.getState().setActiveTool('eyedropper');
            break;
          case 'e':
            useMapStore.getState().setActiveTool('eraser');
            break;
          case 'l':
            useMapStore.getState().setActiveTool('line');
            break;
          case 'r':
            useMapStore.getState().setActiveTool('rectangle');
            break;
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [handleOpenProject, saveNow]);

  // Dialog handlers
  const handleSelectProvince = useCallback((id: number) => {
    setProvinceDialog({ isOpen: true, mode: 'edit', provinceId: id });
  }, []);

  const handleSelectState = useCallback((id: number) => {
    setStateDialog({ isOpen: true, stateId: id });
  }, []);

  const handleSelectRegion = useCallback((id: number) => {
    setRegionDialog({ isOpen: true, regionId: id });
  }, []);

  const handleSelectAIArea = useCallback((name: string) => {
    setAIAreaDialog({ isOpen: true, areaName: name });
  }, []);

  if (isLoading) {
    return (
      <div className="w-full h-full flex items-center justify-center bg-ide-bg">
        <div className="text-ide-text text-lg">Loading project...</div>
      </div>
    );
  }

  // Test mode handler - generates test map for browser debugging
  const handleTestMode = useCallback(() => {
    // Generate test BMP
    const testBMP = generateTestBMP(512, 512);
    loadBMP(testBMP);
    
    // Set up a dummy project
    useProjectStore.setState({
      project: {
        rootPath: '/test',
        mapPath: '/test/map',
        commonPath: '/test/common',
        historyPath: '/test/history',
        loaded: true,
      },
      isLoading: false,
    });
  }, [loadBMP]);

  if (!project) {
    return <WelcomeScreen onOpenProject={handleOpenProject} onTestMode={handleTestMode} />;
  }

  return (
    <div className="w-full h-full flex flex-col bg-ide-bg">
      <Header onOpenProject={handleOpenProject} />
      
      <div className="flex-1 flex overflow-hidden">
        {/* Left Sidebar */}
        <Sidebar />
        
        {/* Main Content - Map Canvas with WebGL */}
        <div className="flex-1 flex flex-col overflow-hidden">
          <WebGLMapCanvas />
        </div>
        
        {/* Right Panel - Tabbed */}
        <div className="w-80 flex flex-col bg-ide-sidebar border-l border-ide-border">
          {/* Tab Headers */}
          <div className="flex border-b border-ide-border overflow-x-auto">
            {[
              { id: 'layers' as const, label: 'Layers' },
              { id: 'properties' as const, label: 'Props' },
              { id: 'search' as const, label: 'Search' },
              { id: 'validation' as const, label: 'Valid' },
              { id: 'countries' as const, label: 'Colors' },
            ].map(({ id, label }) => (
              <button
                key={id}
                className={`flex-shrink-0 px-3 py-2 text-xs font-medium transition-colors ${
                  rightPanelTab === id
                    ? 'text-ide-text bg-ide-active border-b-2 border-blue-500'
                    : 'text-ide-text-muted hover:bg-ide-hover'
                }`}
                onClick={() => setRightPanelTab(id)}
              >
                {label}
              </button>
            ))}
          </div>
          
          {/* Tab Content */}
          <div className="flex-1 overflow-hidden">
            {rightPanelTab === 'layers' && <LayerPanel />}
            {rightPanelTab === 'properties' && <PropertyPanel />}
            {rightPanelTab === 'search' && (
              <SearchPanel
                onSelectProvince={handleSelectProvince}
                onSelectState={handleSelectState}
                onSelectRegion={handleSelectRegion}
                onSelectAIArea={handleSelectAIArea}
              />
            )}
            {rightPanelTab === 'validation' && (
              <ValidationPanel
                onSelectProvince={handleSelectProvince}
                onSelectState={handleSelectState}
                onSelectRegion={handleSelectRegion}
              />
            )}
            {rightPanelTab === 'countries' && <CountryColorsPanel />}
          </div>
          
          {/* Auto-save status */}
          <div className="px-3 py-2 border-t border-ide-border flex items-center justify-between">
            <div className="flex items-center gap-2">
              <button
                onClick={() => setAutoSaveEnabled(!autoSaveEnabled)}
                className={`w-8 h-4 rounded-full transition-colors ${
                  autoSaveEnabled ? 'bg-green-600' : 'bg-gray-600'
                }`}
              >
                <div className={`w-3 h-3 bg-white rounded-full transition-transform ${
                  autoSaveEnabled ? 'translate-x-4' : 'translate-x-0.5'
                }`} />
              </button>
              <span className="text-xs text-ide-text-muted">Auto-save</span>
            </div>
            <div className="flex items-center gap-2">
              {isSaving && (
                <span className="text-xs text-yellow-400">Saving...</span>
              )}
              {pendingChanges && !isSaving && (
                <span className="text-xs text-orange-400">Unsaved</span>
              )}
              {saveError && (
                <span className="text-xs text-red-400" title={saveError}>Error</span>
              )}
              {lastSave && !isSaving && !pendingChanges && (
                <span className="text-xs text-green-400">Saved</span>
              )}
              <button
                onClick={saveNow}
                disabled={isSaving}
                className="px-2 py-0.5 text-xs bg-blue-600 hover:bg-blue-700 
                         disabled:bg-gray-600 text-white rounded"
              >
                Save
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <StatusBar />

      {/* Dialogs */}
      <ProvinceEditorDialog
        isOpen={provinceDialog.isOpen}
        onClose={() => setProvinceDialog({ isOpen: false, mode: 'create' })}
        mode={provinceDialog.mode}
        provinceId={provinceDialog.provinceId}
      />
      
      <StateEditorDialog
        isOpen={stateDialog.isOpen}
        onClose={() => setStateDialog({ isOpen: false, stateId: 0 })}
        stateId={stateDialog.stateId}
      />
      
      <StrategicRegionEditorDialog
        isOpen={regionDialog.isOpen}
        onClose={() => setRegionDialog({ isOpen: false, regionId: 0 })}
        regionId={regionDialog.regionId}
      />
      
      <AIAreaEditorDialog
        isOpen={aiAreaDialog.isOpen}
        onClose={() => setAIAreaDialog({ isOpen: false, areaName: '' })}
        areaName={aiAreaDialog.areaName}
      />
    </div>
  );
};

export default App;
