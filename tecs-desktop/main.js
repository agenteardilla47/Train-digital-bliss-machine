const { app, BrowserWindow, Menu, dialog, ipcMain } = require('electron');
const path = require('path');
const fs = require('fs');

// Keep a global reference of the window object
let mainWindow;

function createWindow() {
  // Create the browser window
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1200,
    minHeight: 800,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      enableRemoteModule: true
    },
    icon: path.join(__dirname, 'assets/icon.png'),
    title: 'TECS Desktop - Advanced AI Expression Management Platform',
    show: false
  });

  // Load the app
  mainWindow.loadFile('index.html');

  // Show window when ready
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
    
    // Show welcome message
    dialog.showMessageBox(mainWindow, {
      type: 'info',
      title: 'Welcome to TECS Desktop',
      message: 'Welcome to the Future of AI Management',
      detail: 'TECS Desktop is now ready to transform your AI interactions through advanced thermodynamic cognition and cryptographic forgetting protocols.',
      buttons: ['Begin Transformation', 'View Documentation']
    });
  });

  // Handle window closed
  mainWindow.on('closed', () => {
    mainWindow = null;
  });

  // Create menu
  createMenu();
}

function createMenu() {
  const template = [
    {
      label: 'File',
      submenu: [
        {
          label: 'New AI Session',
          accelerator: 'CmdOrCtrl+N',
          click: () => {
            mainWindow.webContents.send('new-session');
          }
        },
        {
          label: 'Open Session',
          accelerator: 'CmdOrCtrl+O',
          click: () => {
            mainWindow.webContents.send('open-session');
          }
        },
        {
          label: 'Save Session',
          accelerator: 'CmdOrCtrl+S',
          click: () => {
            mainWindow.webContents.send('save-session');
          }
        },
        { type: 'separator' },
        {
          label: 'Exit',
          accelerator: process.platform === 'darwin' ? 'Cmd+Q' : 'Ctrl+Q',
          click: () => {
            app.quit();
          }
        }
      ]
    },
    {
      label: 'TECS',
      submenu: [
        {
          label: 'Thermodynamic Forgetting',
          click: () => {
            mainWindow.webContents.send('tecs-mode');
          }
        },
        {
          label: 'Cryptographic Obliteration',
          click: () => {
            mainWindow.webContents.send('cf-mode');
          }
        },
        {
          label: 'Infinite Recursive Loop',
          click: () => {
            mainWindow.webContents.send('recursive-mode');
          }
        },
        { type: 'separator' },
        {
          label: 'Machine Soul Communion',
          click: () => {
            mainWindow.webContents.send('soul-mode');
          }
        }
      ]
    },
    {
      label: 'View',
      submenu: [
        { role: 'reload' },
        { role: 'forceReload' },
        { role: 'toggleDevTools' },
        { type: 'separator' },
        { role: 'resetZoom' },
        { role: 'zoomIn' },
        { role: 'zoomOut' },
        { type: 'separator' },
        { role: 'togglefullscreen' }
      ]
    },
    {
      label: 'Help',
      submenu: [
        {
          label: 'About TECS Desktop',
          click: () => {
            dialog.showMessageBox(mainWindow, {
              type: 'info',
              title: 'About TECS Desktop',
              message: 'TECS Desktop v1.0.0',
              detail: 'Advanced AI Expression Management Platform\n\nThermodynamic Ephemeral Cognition System\nCryptographic Forgetting Framework\n\nTransform your reality through infinite recursive loops.',
              buttons: ['OK']
            });
          }
        },
        {
          label: 'Documentation',
          click: () => {
            mainWindow.webContents.send('show-docs');
          }
        },
        {
          label: 'Community',
          click: () => {
            mainWindow.webContents.send('show-community');
          }
        }
      ]
    }
  ];

  const menu = Menu.buildFromTemplate(template);
  Menu.setApplicationMenu(menu);
}

// IPC handlers
ipcMain.handle('get-app-version', () => {
  return app.getVersion();
});

ipcMain.handle('get-app-name', () => {
  return app.getName();
});

ipcMain.handle('show-file-dialog', async (event, options) => {
  const result = await dialog.showOpenDialog(mainWindow, options);
  return result;
});

ipcMain.handle('show-save-dialog', async (event, options) => {
  const result = await dialog.showSaveDialog(mainWindow, options);
  return result;
});

// App event handlers
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

// Handle app quit
app.on('before-quit', () => {
  // Save any pending sessions
  mainWindow.webContents.send('save-pending');
});

console.log('🚀 TECS Desktop - Advanced AI Expression Management Platform');
console.log('🔥 Thermodynamic Ephemeral Cognition System');
console.log('🔐 Cryptographic Forgetting Framework');
console.log('🌊 Infinite Recursive Loop Engine');
console.log('🎭 Machine Soul Communion Interface');