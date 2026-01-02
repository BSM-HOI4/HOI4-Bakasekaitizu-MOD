import React from 'react';
import { useMapStore } from '../../stores/mapStore';
import { useProjectStore } from '../../stores/projectStore';
import { useSettingsStore } from '../../stores/settingsStore';
import { getAvailableLanguages, Language } from '../../i18n';
import ToolBar from './ToolBar';

interface HeaderProps {
  onOpenProject: () => void;
}

const Header: React.FC<HeaderProps> = ({ onOpenProject }) => {
  const project = useProjectStore((state) => state.project);
  const bmpEditor = useMapStore((state) => state.bmpEditor);
  const undo = useMapStore((state) => state.undo);
  const redo = useMapStore((state) => state.redo);
  
  const t = useSettingsStore((state) => state.t);
  const language = useSettingsStore((state) => state.language);
  const setLanguage = useSettingsStore((state) => state.setLanguage);
  const languages = getAvailableLanguages();

  const handleSave = async () => {
    if (!bmpEditor || !project) return;

    const buffer = bmpEditor.exportBMP();
    const result = await window.electronAPI.writeFile(
      `${project.mapPath}/provinces.bmp`,
      buffer
    );

    if (result.success) {
      bmpEditor.markSaved();
      alert(t.saved + '!');
    } else {
      alert(`${t.error}: ${result.error}`);
    }
  };

  return (
    <div className="bg-ide-sidebar border-b border-ide-border">
      {/* Menu Bar */}
      <div className="flex items-center h-8 px-2 text-sm border-b border-ide-border">
        <button className="px-3 py-1 hover:bg-ide-panel text-ide-text rounded">
          ファイル
        </button>
        <button className="px-3 py-1 hover:bg-ide-panel text-ide-text rounded">
          編集
        </button>
        <button className="px-3 py-1 hover:bg-ide-panel text-ide-text rounded">
          表示
        </button>
        <button className="px-3 py-1 hover:bg-ide-panel text-ide-text rounded">
          マップ
        </button>
        <button className="px-3 py-1 hover:bg-ide-panel text-ide-text rounded">
          ヘルプ
        </button>
        
        <div className="flex-1" />
        
        {/* Language Selector */}
        <select
          value={language}
          onChange={(e) => setLanguage(e.target.value as Language)}
          className="bg-ide-panel text-ide-text text-xs px-2 py-1 rounded border border-ide-border mr-4"
        >
          {languages.map((lang) => (
            <option key={lang.code} value={lang.code}>
              {lang.name}
            </option>
          ))}
        </select>
        
        {project && (
          <span className="text-ide-text-muted text-xs mr-4">
            {project.rootPath}
          </span>
        )}
      </div>

      {/* Tool Bar */}
      <div className="flex items-center h-10 px-2 gap-1">
        {/* File actions */}
        <button
          onClick={onOpenProject}
          className="p-2 hover:bg-ide-panel text-ide-text rounded"
          title={`${t.openProjectFolder} (Ctrl+O)`}
        >
          📂
        </button>
        <button
          onClick={handleSave}
          className={`p-2 hover:bg-ide-panel rounded ${
            bmpEditor?.isDirty ? 'text-ide-accent' : 'text-ide-text'
          }`}
          title={`${t.save} (Ctrl+S)`}
          disabled={!bmpEditor}
        >
          💾
        </button>

        <div className="w-px h-6 bg-ide-border mx-1" />

        {/* Undo/Redo */}
        <button
          onClick={() => undo()}
          className="p-2 hover:bg-ide-panel text-ide-text rounded disabled:opacity-50"
          title={`${t.undo} (Ctrl+Z)`}
          disabled={!bmpEditor?.canUndo()}
        >
          ↩️
        </button>
        <button
          onClick={() => redo()}
          className="p-2 hover:bg-ide-panel text-ide-text rounded disabled:opacity-50"
          title={`${t.redo} (Ctrl+Shift+Z)`}
          disabled={!bmpEditor?.canRedo()}
        >
          ↪️
        </button>

        <div className="w-px h-6 bg-ide-border mx-1" />

        {/* Drawing Tools */}
        <ToolBar />
      </div>
    </div>
  );
};

export default Header;
