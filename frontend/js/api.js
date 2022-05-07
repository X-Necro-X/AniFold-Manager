const { PythonShell } = require('python-shell');
const { MAIN } = require('../constants/constants');

exports.connectBackend = () => {
	const script = new PythonShell(MAIN.PYTHON_MAIN, {
		mode: 'json',
	});
	script.send({
		'key': 'value'
	});
	script.on('message', (message) => {
		console.log(message);
	});
	script.end((err) => {
		if (err) {
			console.log(err);
		}
	});
};
