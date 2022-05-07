const { app, BrowserWindow } = require('electron');
const { MAIN } = require('./frontend/constants/constants');
const { connectBackend } = require('./frontend/js/api');

const createWindow = () => {
	const win = new BrowserWindow({
		width: 800,
		height: 800,
	});
	win.loadFile(MAIN.INDEX_FILE);
	connectBackend();
};

app.whenReady().then(() => {
	createWindow();
});

app.on('window-all-closed', () => {
	if (process.platform !== 'darwin') app.quit();
});
