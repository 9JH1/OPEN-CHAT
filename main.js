const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const fs = require('fs');
const { execFile } = require('child_process');

let child;

function startChildProcess() {
    child = execFile(path.join(__dirname, 'main.exe'), [], {
        detached: true,
        stdio: 'ignore',
    });

    child.unref();

    child.on('exit', (code) => {
        console.log(`main.exe exited with code ${code}`);
    });

    child.on('error', (error) => {
        console.error(`Error starting main.exe: ${error}`);
    });
}




const createWindow = () => {
    const win = new BrowserWindow({
        width: 320,
        height: 555,
        resizable: false,
        maximizable: false,
        fullscreenable: false,
        autoHideMenuBar: true,
        titleBarStyle: 'hidden',
        titleBarOverlay: {
            color: 'black',
            symbolColor: '#482E82',
        },
        webPreferences: {
            nodeIntegration: true
        }
    });

    win.loadFile('templates/index.html');
};

function getData(endpoint) {
    return fetch(`http://127.0.0.1:5000${endpoint}`)
        .then((res) => res.text())
        .catch((error) => {
            console.error(error);
        });
};

app.whenReady().then(() => {


    createWindow();
    startChildProcess();

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
            startChildProcess();
        }
    });

    app.on('before-quit', () => {
        getData("/stopServer");
    });
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});
