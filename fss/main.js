// ./main.js
const { app, BrowserWindow, Menu } = require('electron')
const path = require('path');
const url = require('url');

let win = null;

//require('electron-debug')({ showDevTools: true });

var template = [{
    label: "Application",
    submenu: [
        { label: "About Application", selector: "orderFrontStandardAboutPanel:" },
        { type: "separator" },
        { label: "Quit", accelerator: "CmdOrCtrl+Q", click: function () { app.quit(); } }
    ]
}, {
    label: "Edit",
    submenu: [
        { label: "Undo", accelerator: "CmdOrCtrl+Z", selector: "undo:" },
        { label: "Redo", accelerator: "Shift+CmdOrCtrl+Z", selector: "redo:" },
        { type: "separator" },
        { label: "Cut", accelerator: "CmdOrCtrl+X", selector: "cut:" },
        { label: "Copy", accelerator: "CmdOrCtrl+C", selector: "copy:" },
        { label: "Paste", accelerator: "CmdOrCtrl+V", selector: "paste:" },
        { label: "Select All", accelerator: "CmdOrCtrl+A", selector: "selectAll:" }
    ]
},
{
    label: 'View',
    submenu: [
        { role: 'reload' },
        { role: 'forcereload' },
        { role: 'toggledevtools' },
        { type: 'separator' },
        { role: 'resetzoom' },
        { role: 'zoomin' },
        { role: 'zoomout' },
        { type: 'separator' },
        { role: 'togglefullscreen' }
    ]
},
{
    role: 'window',
    submenu: [
        { role: 'minimize' },
        { role: 'close' }
    ]
},
];

const menu = Menu.buildFromTemplate(template)

app.on('ready', function () {

    // Initialize the window to our specified dimensions
    win = new BrowserWindow({ width: 1000, height: 600 });
    Menu.setApplicationMenu(menu)

    // Specify entry point
    win.loadURL(url.format({
        pathname: path.join(__dirname, 'dist/index.html'),
        protocol: 'file:',
        slashes: true
    }));

    // Close window when x is clicked
    win.on('closed', function () {
        win = null;
    });

});

// Create window when launched
app.on('activate', () => {
    if (win === null) {
        createWindow()
    }
});

// Exit app when all windows are closed
app.on('window-all-closed', function () {
    if (process.platform != 'darwin') {
        app.quit();
    }
});
