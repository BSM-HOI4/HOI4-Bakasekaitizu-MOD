import React from 'react';
import { useSettingsStore } from '../stores/settingsStore';

interface WelcomeScreenProps {
  onOpenProject: () => void;
  onTestMode?: () => void;
}

const WelcomeScreen: React.FC<WelcomeScreenProps> = ({ onOpenProject, onTestMode }) => {
  const t = useSettingsStore((state) => state.t);
  
  return (
    <div className="w-full h-full flex items-center justify-center bg-ide-bg">
      <div className="max-w-lg text-center">
        <h1 className="text-4xl font-bold text-ide-text mb-4">
          {t.welcomeTitle}
        </h1>
        <p className="text-ide-text-muted mb-8">
          {t.welcomeSubtitle}
        </p>
        
        <div className="bg-ide-panel p-8 rounded-lg border border-ide-border">
          <h2 className="text-xl text-ide-text mb-4">{t.getStarted}</h2>
          <p className="text-ide-text-muted mb-6 text-sm">
            {t.welcomeDescription}
          </p>
          
          <button
            onClick={onOpenProject}
            className="px-6 py-3 bg-ide-accent text-white rounded hover:bg-ide-accent-hover transition-colors"
          >
            {t.openModFolder}
          </button>
          
          {onTestMode && (
            <button
              onClick={onTestMode}
              className="ml-4 px-6 py-3 bg-green-600 text-white rounded hover:bg-green-700 transition-colors"
            >
              {t.testMode}
            </button>
          )}
          
          <div className="mt-6 text-xs text-ide-text-muted">
            <p>{t.keyboardShortcut}: <kbd className="px-2 py-1 bg-ide-bg rounded">Ctrl/Cmd + O</kbd></p>
          </div>
        </div>

        <div className="mt-8 grid grid-cols-2 gap-4 text-left">
          <div className="bg-ide-sidebar p-4 rounded border border-ide-border">
            <h3 className="text-ide-text font-semibold mb-2">📍 {t.provinceEditing}</h3>
            <p className="text-ide-text-muted text-xs">
              {t.provinceEditingDesc}
            </p>
          </div>
          <div className="bg-ide-sidebar p-4 rounded border border-ide-border">
            <h3 className="text-ide-text font-semibold mb-2">🗺️ {t.stateManagement}</h3>
            <p className="text-ide-text-muted text-xs">
              {t.stateManagementDesc}
            </p>
          </div>
          <div className="bg-ide-sidebar p-4 rounded border border-ide-border">
            <h3 className="text-ide-text font-semibold mb-2">🌍 {t.strategicRegions}</h3>
            <p className="text-ide-text-muted text-xs">
              {t.strategicRegionsDesc}
            </p>
          </div>
          <div className="bg-ide-sidebar p-4 rounded border border-ide-border">
            <h3 className="text-ide-text font-semibold mb-2">🤖 {t.aiAreas}</h3>
            <p className="text-ide-text-muted text-xs">
              {t.aiAreasDesc}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WelcomeScreen;
