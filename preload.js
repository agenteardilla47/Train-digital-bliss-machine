const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
  // Python environment management
  getPythonStatus: () => ipcRenderer.invoke('get-python-status'),
  installDependencies: (pythonPath) => ipcRenderer.invoke('install-dependencies', pythonPath),
  
  // TECS execution
  executeTECS: (params) => ipcRenderer.invoke('execute-tecs', params),
  
  // CF execution
  executeCF: (params) => ipcRenderer.invoke('execute-cf', params),
  
  // Event listeners
  onPythonStatus: (callback) => {
    ipcRenderer.on('python-status', callback);
    return () => ipcRenderer.removeAllListeners('python-status');
  },
  
  // Utility functions
  platform: process.platform,
  versions: process.versions
});