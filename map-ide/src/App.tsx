import React, { useCallback, useEffect } from 'react';
import { useProjectStore } from './stores/projectStore';
import { useMapStore } from './stores/mapStore';
import Header from './components/layout/Header';
import Sidebar from './components/layout/Sidebar';
import StatusBar from './components/layout/StatusBar';
import MapCanvas from './components/map/MapCanvas';
import PropertyPanel from './components/panels/PropertyPanel';
import WelcomeScreen from './components/WelcomeScreen';

const App: React.FC = () => {
  const project = useProjectStore((state) => state.project);
  const openProject = useProjectStore((state) => state.openProject);
  const isLoading = useProjectStore((state) => state.isLoading);
  const loadBMP = useMapStore((state) => state.loadBMP);

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

      const bmpPath = `${project.mapPath}/provinces.bmp`;
      const result = await window.electronAPI.readFile(bmpPath);
      
      if (result.success && result.data) {
        loadBMP(result.data);
      }
    };

    loadMapBMP();
  }, [project, loadBMP]);

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Ctrl/Cmd + O: Open project
      if ((e.ctrlKey || e.metaKey) && e.key === 'o') {
        e.preventDefault();
        handleOpenProject();
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
  }, [handleOpenProject]);

  if (isLoading) {
    return (
      <div className="w-full h-full flex items-center justify-center bg-ide-bg">
        <div className="text-ide-text text-lg">Loading project...</div>
      </div>
    );
  }

  if (!project) {
    return <WelcomeScreen onOpenProject={handleOpenProject} />;
  }

  return (
    <div className="w-full h-full flex flex-col bg-ide-bg">
      <Header onOpenProject={handleOpenProject} />
      
      <div className="flex-1 flex overflow-hidden">
        {/* Left Sidebar */}
        <Sidebar />
        
        {/* Main Content - Map Canvas */}
        <div className="flex-1 flex flex-col overflow-hidden">
          <MapCanvas />
        </div>
        
        {/* Right Panel - Properties */}
        <PropertyPanel />
      </div>
      
      <StatusBar />
    </div>
  );
};

export default App;
