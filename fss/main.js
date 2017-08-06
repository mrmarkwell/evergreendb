// ./main.js
const {app, BrowserWindow} = require('electron')
const path = require('path');
const url = require('url');

let win = null;

app.on('ready', function () {

	// Initialize the window to our specified dimensions
	win = new BrowserWindow({width: 1000, height: 600});

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
