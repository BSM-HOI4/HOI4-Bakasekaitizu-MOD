import React from 'react';

interface WelcomeScreenProps {
  onOpenProject: () => void;
}

const WelcomeScreen: React.FC<WelcomeScreenProps> = ({ onOpenProject }) => {
  return (
    <div className="w-full h-full flex items-center justify-center bg-ide-bg">
      <div className="max-w-lg text-center">
        <h1 className="text-4xl font-bold text-ide-text mb-4">
          HoI4 Map IDE
        </h1>
        <p className="text-ide-text-muted mb-8">
          Hearts of Iron 4 Map Integrated Development Environment
        </p>
        
        <div className="bg-ide-panel p-8 rounded-lg border border-ide-border">
          <h2 className="text-xl text-ide-text mb-4">Get Started</h2>
          <p className="text-ide-text-muted mb-6 text-sm">
            Open a HoI4 mod folder to begin editing. The folder should contain
            the standard mod structure with <code className="text-ide-accent">map/</code>,{' '}
            <code className="text-ide-accent">common/</code>, and{' '}
            <code className="text-ide-accent">history/</code> directories.
          </p>
          
          <button
            onClick={onOpenProject}
            className="px-6 py-3 bg-ide-accent text-white rounded hover:bg-ide-accent-hover transition-colors"
          >
            Open Mod Folder
          </button>
          
          <div className="mt-6 text-xs text-ide-text-muted">
            <p>Keyboard shortcut: <kbd className="px-2 py-1 bg-ide-bg rounded">Ctrl/Cmd + O</kbd></p>
          </div>
        </div>

        <div className="mt-8 grid grid-cols-2 gap-4 text-left">
          <div className="bg-ide-sidebar p-4 rounded border border-ide-border">
            <h3 className="text-ide-text font-semibold mb-2">📍 Province Editing</h3>
            <p className="text-ide-text-muted text-xs">
              Edit provinces.bmp directly with brush, fill, and selection tools
            </p>
          </div>
          <div className="bg-ide-sidebar p-4 rounded border border-ide-border">
            <h3 className="text-ide-text font-semibold mb-2">🗺️ State Management</h3>
            <p className="text-ide-text-muted text-xs">
              Manage states, assign provinces, and edit properties
            </p>
          </div>
          <div className="bg-ide-sidebar p-4 rounded border border-ide-border">
            <h3 className="text-ide-text font-semibold mb-2">🌍 Strategic Regions</h3>
            <p className="text-ide-text-muted text-xs">
              View and edit strategic regions with weather settings
            </p>
          </div>
          <div className="bg-ide-sidebar p-4 rounded border border-ide-border">
            <h3 className="text-ide-text font-semibold mb-2">🤖 AI Areas</h3>
            <p className="text-ide-text-muted text-xs">
              Configure AI areas for strategic region grouping
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WelcomeScreen;
