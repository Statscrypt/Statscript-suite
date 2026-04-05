const { app, BrowserWindow, ipcMain, Menu, dialog } = require('electron');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

let pythonProcess = null;
let mainWindow = null;
let graphWindow = null;

function createGraphWindow() {
  if (graphWindow) {
    graphWindow.focus();
    return;
  }

  graphWindow = new BrowserWindow({
    height: 600,
    width: 800,
    title: 'Statscrypt Graph',
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    }
  });

  graphWindow.loadFile(path.join(__dirname, 'graph.html'));

  graphWindow.on('closed', () => {
    graphWindow = null;
  });
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: true, // Be cautious with this in production
      contextIsolation: false // Be cautious with this in production
    }
  });

  mainWindow.loadFile(path.join(__dirname, 'index.html'));

  // Open developer tools in debug mode
  // mainWindow.webContents.openDevTools();

  // Define the path to the Python executable
  // In development, we use the locally built executable in resources/engine
  const pythonExecutable = app.isPackaged
    ? path.join(process.resourcesPath, 'engine', 'statscrypt_engine', 'statscrypt_engine')
    : path.join(__dirname, '..', 'resources', 'engine', 'statscrypt_engine', 'statscrypt_engine.exe');

  const scriptArgs = ['--json'];

  console.log(`[DEBUG] Python executable path: ${pythonExecutable}`);
  console.log(`[DEBUG] Starting statscrypt engine...`);

  // Spawn the Python statscrypt CLI in JSON mode
  // Note: The path to the python executable might need to be adjusted based on the system.
  // A bundled python is the most reliable solution.
  pythonProcess = spawn(pythonExecutable, scriptArgs);

  pythonProcess.on('error', (err) => {
    console.error(`[ERROR] Failed to start Python process: ${err}`);
    mainWindow.webContents.send('stata-output', `[FATAL ERROR] Failed to start Python engine: ${err.message}\n`);
  });

  let outputBuffer = "";
  pythonProcess.stdout.on('data', (data) => {
    outputBuffer += data.toString();
    console.log(`[PYTHON] ${data.toString()}`);
    // Attempt to parse complete JSON messages
    let lastNewlineIndex;
    while ((lastNewlineIndex = outputBuffer.indexOf('\n')) !== -1) {
      const message = outputBuffer.substring(0, lastNewlineIndex);
      outputBuffer = outputBuffer.substring(lastNewlineIndex + 1);

      try {
        const parsed = JSON.parse(message);
        if (parsed.type === "variable_update") {
          mainWindow.webContents.send('variable-update', parsed.payload);
        } else if (parsed.type === "plot_update") {
            createGraphWindow();
            // Wait for the window to be ready before sending data
            graphWindow.webContents.on('did-finish-load', () => {
                graphWindow.webContents.send('plot-data', parsed.payload);
            });
        }
        else if (parsed.type === "output" || parsed.type === "error") {
          mainWindow.webContents.send('stata-output', parsed.payload + '\n');
        } else if (parsed.type === "ready") {
            mainWindow.webContents.send('stata-output', parsed.payload + '\n');
        }
        // Handle other message types if needed
      } catch (e) {
        // Not a complete JSON object or malformed JSON, treat as raw output for now
        mainWindow.webContents.send('stata-output', message + '\n');
      }
    }
  });

  pythonProcess.stderr.on('data', (data) => {
    // Send stderr as an error output to the GUI
    console.error(`[PYTHON_STDERR] ${data.toString()}`);
    mainWindow.webContents.send('stata-output', `[ENGINE ERROR] ${data.toString()}`);
  });

  pythonProcess.on('exit', (code) => {
    console.log(`[INFO] Python process exited with code ${code}`);
  });
}

function createMenu() {
  const template = [
    {
      label: 'File',
      submenu: [
        {
          label: 'Open File',
          accelerator: 'CmdOrCtrl+O',
          click: async () => {
            const result = await dialog.showOpenDialog(mainWindow, {
              properties: ['openFile'],
              filters: [
                { name: 'CSV Files', extensions: ['csv'] },
                { name: 'All Files', extensions: ['*'] }
              ]
            });

            if (!result.canceled && result.filePaths.length > 0) {
              const filePath = result.filePaths[0];
              // Send use command to Python engine
              const command = `use "${filePath}"`;
              console.log(`[MENU] Sending command: ${command}`);
              if (pythonProcess && pythonProcess.stdin && !pythonProcess.stdin.destroyed) {
                const message = JSON.stringify({ task: 'EXECUTE', payload: command });
                console.log(`[MENU-SEND] ${message}`);
                pythonProcess.stdin.write(message + '\n');
              } else {
                mainWindow.webContents.send('stata-output', '[ERROR] Python engine is not running\n');
              }
            }
          }
        },
        {
          label: 'Exit',
          accelerator: 'CmdOrCtrl+Q',
          click: () => {
            app.quit();
          }
        }
      ]
    },
    {
      label: 'Tools',
      submenu: [
        {
          label: 'Developer Tools',
          accelerator: 'F12',
          click: () => {
            if (mainWindow) {
              mainWindow.webContents.toggleDevTools();
            }
          }
        }
      ]
    },
    {
      label: 'Help',
      submenu: [
        {
          label: 'Commands Help',
          click: () => {
            mainWindow.webContents.send('stata-output', '\n=== Statscrypt Available Commands ===\n' +
              'use "filepath"         - Load a CSV file\n' +
              'summarize [vars]       - Summary statistics\n' +
              'list [vars]            - List first 20 rows\n' +
              'gen newvar = oldvar    - Generate new variable\n' +
              'graph varname          - Create a graph\n' +
              'summarize if condition - Filter with conditions\n' +
              '===================================\n');
          }
        }
      ]
    }
  ];

  Menu.setApplicationMenu(Menu.buildFromTemplate(template));
}

// Receive command from UI and send to Python
ipcMain.on('run-command', (event, command) => {
  if (pythonProcess && pythonProcess.stdin && !pythonProcess.stdin.destroyed) {
    const message = JSON.stringify({ task: 'EXECUTE', payload: command });
    console.log(`[SEND] ${message}`);
    pythonProcess.stdin.write(message + '\n');
  } else {
    console.error('[ERROR] Python process is not running or stdin is not available');
    mainWindow.webContents.send('stata-output', 'Error: Python engine is not running.');
  }
});

app.whenReady().then(() => {
  createWindow();
  createMenu();
});

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

// Make sure to kill the python process when the app quits
app.on('will-quit', () => {
  if (pythonProcess) {
    console.log('[INFO] Terminating Python process...');
    pythonProcess.kill();
  }
});
