const { app, BrowserWindow, ipcMain, dialog, shell } = require('electron');
const path = require('path');
const fs = require('fs');
const { PythonShell } = require('python-shell');

let mainWindow;
let pythonProcess = null;

function createWindow() {
  // Create the browser window
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1200,
    minHeight: 800,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      enableRemoteModule: false,
      preload: path.join(__dirname, 'preload.js')
    },
    icon: path.join(__dirname, 'assets', 'icon.png'),
    title: 'TECS Desktop - Thermodynamic Ephemeral Cognition System',
    show: false
  });

  // Load the app
  mainWindow.loadFile('index.html');

  // Show window when ready
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
    
    // Check if Python environment is ready
    checkPythonEnvironment();
  });

  // Handle window closed
  mainWindow.on('closed', () => {
    mainWindow = null;
  });

  // Handle external links
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url);
    return { action: 'deny' };
  });
}

function checkPythonEnvironment() {
  const pythonPath = getPythonPath();
  
  if (pythonPath) {
    // Check if required packages are installed
    checkPythonDependencies(pythonPath);
  } else {
    mainWindow.webContents.send('python-status', {
      status: 'not-found',
      message: 'Python not found. Please install Python 3.8+ and try again.'
    });
  }
}

function getPythonPath() {
  // Try to find Python in common locations
  const possiblePaths = [
    'python3',
    'python',
    path.join(process.resourcesPath, 'python', 'python.exe'), // Windows
    path.join(process.resourcesPath, 'python', 'bin', 'python3'), // Linux/Mac
  ];

  for (const pythonPath of possiblePaths) {
    try {
      // Simple check if Python exists
      if (fs.existsSync(pythonPath) || require('child_process').execSync(`which ${pythonPath}`, { stdio: 'ignore' })) {
        return pythonPath;
      }
    } catch (e) {
      // Continue to next path
    }
  }
  
  return null;
}

function checkPythonDependencies(pythonPath) {
  const requirementsPath = path.join(process.resourcesPath, 'requirements_minimal.txt');
  
  if (!fs.existsSync(requirementsPath)) {
    mainWindow.webContents.send('python-status', {
      status: 'no-requirements',
      message: 'Requirements file not found.'
    });
    return;
  }

  // Check if packages are installed
  const checkScript = `
import sys
import importlib

required_packages = ['numpy', 'scipy', 'torch', 'cryptography']
missing_packages = []

for package in required_packages:
    try:
        importlib.import_module(package)
    except ImportError:
        missing_packages.append(package)

if missing_packages:
    print("MISSING:" + ",".join(missing_packages))
else:
    print("READY")
`;

  const options = {
    mode: 'text',
    pythonPath: pythonPath,
    pythonOptions: ['-u'],
    scriptPath: '.',
    args: []
  };

  PythonShell.runString(checkScript, options, (err, results) => {
    if (err) {
      mainWindow.webContents.send('python-status', {
        status: 'error',
        message: `Error checking dependencies: ${err.message}`
      });
      return;
    }

    if (results && results[0] === 'READY') {
      mainWindow.webContents.send('python-status', {
        status: 'ready',
        message: 'Python environment ready!'
      });
    } else if (results && results[0].startsWith('MISSING:')) {
      const missing = results[0].replace('MISSING:', '');
      mainWindow.webContents.send('python-status', {
        status: 'missing-deps',
        message: `Missing packages: ${missing}`,
        missing: missing.split(',')
      });
    }
  });
}

// Install Python dependencies
ipcMain.handle('install-dependencies', async (event, pythonPath) => {
  try {
    const requirementsPath = path.join(process.resourcesPath, 'requirements_minimal.txt');
    
    if (!fs.existsSync(requirementsPath)) {
      throw new Error('Requirements file not found');
    }

    return new Promise((resolve, reject) => {
      const options = {
        mode: 'text',
        pythonPath: pythonPath,
        pythonOptions: ['-m', 'pip', 'install', '-r', requirementsPath],
        scriptPath: '.',
        args: []
      };

      PythonShell.runString('', options, (err, results) => {
        if (err) {
          reject(err);
        } else {
          resolve({ success: true, message: 'Dependencies installed successfully!' });
        }
      });
    });
  } catch (error) {
    throw error;
  }
});

// Execute TECS protocol
ipcMain.handle('execute-tecs', async (event, { sourceData, collaboratorProfile, securityLevel }) => {
  try {
    const pythonPath = getPythonPath();
    if (!pythonPath) {
      throw new Error('Python not found');
    }

    // Create temporary Python script
    const script = `
import sys
import os
sys.path.append(os.path.join('${process.resourcesPath}', 'cf'))

from thermodynamics import TECS
import json

try:
    # Initialize TECS
    tecs = TECS(security_parameter=${securityLevel}, use_tee=False)
    
    # Execute TECS protocol
    result = tecs.generate('${sourceData.replace(/'/g, "\\'")}', ${JSON.stringify(collaboratorProfile)})
    
    # Convert numpy arrays to lists for JSON serialization
    if 'resonance_commitment' in result:
        result['resonance_commitment'] = str(result['resonance_commitment'])
    
    print("RESULT:" + json.dumps(result))
    
except Exception as e:
    print("ERROR:" + str(e))
`;

    const options = {
      mode: 'text',
      pythonPath: pythonPath,
      pythonOptions: ['-u'],
      scriptPath: '.',
      args: []
    };

    return new Promise((resolve, reject) => {
      PythonShell.runString(script, options, (err, results) => {
        if (err) {
          reject(err);
          return;
        }

        if (results && results.length > 0) {
          const lastResult = results[results.length - 1];
          
          if (lastResult.startsWith('RESULT:')) {
            try {
              const resultData = JSON.parse(lastResult.replace('RESULT:', ''));
              resolve(resultData);
            } catch (parseError) {
              reject(new Error(`Failed to parse result: ${parseError.message}`));
            }
          } else if (lastResult.startsWith('ERROR:')) {
            reject(new Error(lastResult.replace('ERROR:', '')));
          }
        } else {
          reject(new Error('No results from TECS execution'));
        }
      });
    });
  } catch (error) {
    throw error;
  }
});

// Execute CF protocol
ipcMain.handle('execute-cf', async (event, { sourceData, functionalRequirements, securityLevel }) => {
  try {
    const pythonPath = getPythonPath();
    if (!pythonPath) {
      throw new Error('Python not found');
    }

    // Create temporary Python script
    const script = `
import sys
import os
sys.path.append(os.path.join('${process.resourcesPath}', 'cf'))

from core import CryptographicForgetting
import json

try:
    # Initialize CF
    cf = CryptographicForgetting(security_parameter=${securityLevel}, use_tee=False)
    
    # Execute CF protocol
    result = cf.forget('${sourceData.replace(/'/g, "\\'")}', ${JSON.stringify(functionalRequirements)})
    
    # Convert to dict for JSON serialization
    result_dict = {
        'output': str(result.output),
        'proof_size': len(result.proof),
        'certificates_count': len(result.deletion_certificates),
        'performance_metrics': result.performance_metrics.get_performance_summary(),
        'security_parameters': {
            'security_parameter': result.security_parameters.security_parameter,
            'use_tee': result.security_parameters.use_tee,
            'mutual_info_penalty': result.security_parameters.mutual_info_penalty
        }
    }
    
    print("RESULT:" + json.dumps(result_dict))
    
except Exception as e:
    print("ERROR:" + str(e))
`;

    const options = {
      mode: 'text',
      pythonPath: pythonPath,
      pythonOptions: ['-u'],
      scriptPath: '.',
      args: []
    };

    return new Promise((resolve, reject) => {
      PythonShell.runString(script, options, (err, results) => {
        if (err) {
          reject(err);
          return;
        }

        if (results && results.length > 0) {
          const lastResult = results[results.length - 1];
          
          if (lastResult.startsWith('RESULT:')) {
            try {
              const resultData = JSON.parse(lastResult.replace('RESULT:', ''));
              resolve(resultData);
            } catch (parseError) {
              reject(new Error(`Failed to parse result: ${parseError.message}`));
            }
          } else if (lastResult.startsWith('ERROR:')) {
            reject(new Error(lastResult.replace('ERROR:', '')));
          }
        } else {
          reject(new Error('No results from CF execution'));
        }
      });
    });
  } catch (error) {
    throw error;
  }
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

// Quit when all windows are closed
app.on('before-quit', () => {
  if (pythonProcess) {
    pythonProcess.kill();
  }
});