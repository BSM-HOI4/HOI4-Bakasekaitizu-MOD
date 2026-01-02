// Type definitions for Electron API exposed via preload
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

export {};
