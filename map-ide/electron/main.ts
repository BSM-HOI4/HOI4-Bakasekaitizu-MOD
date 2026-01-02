import { app, BrowserWindow, ipcMain, dialog } from 'electron';
import * as path from 'path';
import * as fs from 'fs';

let mainWindow: BrowserWindow | null = null;

const createWindow = () => {
  mainWindow = new BrowserWindow({
    width: 1600,
    height: 1000,
    minWidth: 1200,
    minHeight: 800,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
    backgroundColor: '#1e1e1e',
    show: false,
  });

  // Development or production URL
  if (process.env.VITE_DEV_SERVER_URL) {
    mainWindow.loadURL(process.env.VITE_DEV_SERVER_URL);
    mainWindow.webContents.openDevTools();
  } else {
    mainWindow.loadFile(path.join(__dirname, '../dist/index.html'));
  }

  mainWindow.once('ready-to-show', () => {
    mainWindow?.show();
  });

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
};

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

// IPC Handlers

// Open folder dialog
ipcMain.handle('dialog:openFolder', async () => {
  const result = await dialog.showOpenDialog(mainWindow!, {
    properties: ['openDirectory'],
    title: 'Select HoI4 Mod Folder',
  });
  return result.canceled ? null : result.filePaths[0];
});

// Read file
ipcMain.handle('fs:readFile', async (_, filePath: string) => {
  try {
    const data = await fs.promises.readFile(filePath);
    return { success: true, data: data.buffer };
  } catch (error) {
    return { success: false, error: String(error) };
  }
});

// Read text file
ipcMain.handle('fs:readTextFile', async (_, filePath: string) => {
  try {
    const data = await fs.promises.readFile(filePath, 'utf-8');
    return { success: true, data };
  } catch (error) {
    return { success: false, error: String(error) };
  }
});

// Write file
ipcMain.handle('fs:writeFile', async (_, filePath: string, data: ArrayBuffer) => {
  try {
    await fs.promises.writeFile(filePath, Buffer.from(data));
    return { success: true };
  } catch (error) {
    return { success: false, error: String(error) };
  }
});

// Write text file
ipcMain.handle('fs:writeTextFile', async (_, filePath: string, data: string) => {
  try {
    await fs.promises.writeFile(filePath, data, 'utf-8');
    return { success: true };
  } catch (error) {
    return { success: false, error: String(error) };
  }
});

// Read directory
ipcMain.handle('fs:readDir', async (_, dirPath: string) => {
  try {
    const entries = await fs.promises.readdir(dirPath, { withFileTypes: true });
    return {
      success: true,
      data: entries.map(e => ({
        name: e.name,
        isDirectory: e.isDirectory(),
        isFile: e.isFile(),
      })),
    };
  } catch (error) {
    return { success: false, error: String(error) };
  }
});

// Check file exists
ipcMain.handle('fs:exists', async (_, filePath: string) => {
  try {
    await fs.promises.access(filePath);
    return true;
  } catch {
    return false;
  }
});

// Get file stats
ipcMain.handle('fs:stat', async (_, filePath: string) => {
  try {
    const stats = await fs.promises.stat(filePath);
    return {
      success: true,
      data: {
        size: stats.size,
        isDirectory: stats.isDirectory(),
        isFile: stats.isFile(),
        mtime: stats.mtime.toISOString(),
      },
    };
  } catch (error) {
    return { success: false, error: String(error) };
  }
});
