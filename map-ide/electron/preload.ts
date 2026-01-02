import { contextBridge, ipcRenderer } from 'electron';

// Expose protected methods to renderer process
contextBridge.exposeInMainWorld('electronAPI', {
  // Dialog
  openFolder: () => ipcRenderer.invoke('dialog:openFolder'),
  
  // File system operations
  readFile: (filePath: string) => ipcRenderer.invoke('fs:readFile', filePath),
  readTextFile: (filePath: string) => ipcRenderer.invoke('fs:readTextFile', filePath),
  writeFile: (filePath: string, data: ArrayBuffer) => ipcRenderer.invoke('fs:writeFile', filePath, data),
  writeTextFile: (filePath: string, data: string) => ipcRenderer.invoke('fs:writeTextFile', filePath, data),
  readDir: (dirPath: string) => ipcRenderer.invoke('fs:readDir', dirPath),
  exists: (filePath: string) => ipcRenderer.invoke('fs:exists', filePath),
  stat: (filePath: string) => ipcRenderer.invoke('fs:stat', filePath),
});

// Type definitions for TypeScript
export interface ElectronAPI {
  openFolder: () => Promise<string | null>;
  readFile: (filePath: string) => Promise<{ success: boolean; data?: ArrayBuffer; error?: string }>;
  readTextFile: (filePath: string) => Promise<{ success: boolean; data?: string; error?: string }>;
  writeFile: (filePath: string, data: ArrayBuffer) => Promise<{ success: boolean; error?: string }>;
  writeTextFile: (filePath: string, data: string) => Promise<{ success: boolean; error?: string }>;
  readDir: (dirPath: string) => Promise<{
    success: boolean;
    data?: { name: string; isDirectory: boolean; isFile: boolean }[];
    error?: string;
  }>;
  exists: (filePath: string) => Promise<boolean>;
  stat: (filePath: string) => Promise<{
    success: boolean;
    data?: { size: number; isDirectory: boolean; isFile: boolean; mtime: string };
    error?: string;
  }>;
}

declare global {
  interface Window {
    electronAPI: ElectronAPI;
  }
}
