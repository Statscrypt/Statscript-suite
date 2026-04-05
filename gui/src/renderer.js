const { ipcRenderer } = require('electron');

document.addEventListener('DOMContentLoaded', () => {
    const commandInput = document.getElementById('cmd-input');
    const resultsOutput = document.getElementById('results');
    const historyContainer = document.querySelector('.history-content');
    const commandHistory = [];
    let historyIndex = -1;

    resultsOutput.textContent = '';

    commandInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            const command = commandInput.value.trim();
            console.log(`[RENDERER] Enter pressed with command: "${command}"`);

            if (command) {
                console.log(`[RENDERER] Sending command to main process...`);
                ipcRenderer.send('run-command', command);

                commandHistory.push(command);
                historyIndex = -1;

                const historyEntry = document.createElement('div');
                historyEntry.className = 'command-entry';
                historyEntry.textContent = '> ' + command;
                historyContainer.appendChild(historyEntry);
                historyContainer.scrollTop = historyContainer.scrollHeight;


                commandInput.value = '';
                console.log(`[RENDERER] Input field cleared`);

                resultsOutput.scrollTop = resultsOutput.scrollHeight;
            } else {
                console.log(`[RENDERER] Empty command, not sending`);
            }
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            if (historyIndex < commandHistory.length - 1) {
                historyIndex++;
                commandInput.value = commandHistory[commandHistory.length - 1 - historyIndex];
            }
        } else if (e.key === 'ArrowDown') {
            e.preventDefault();
            if (historyIndex > 0) {
                historyIndex--;
                commandInput.value = commandHistory[commandHistory.length - 1 - historyIndex];
            } else if (historyIndex === 0) {
                historyIndex = -1;
                commandInput.value = '';
            }
        }
    });


    ipcRenderer.on('stata-output', (event, data) => {
        resultsOutput.textContent += data;
        resultsOutput.scrollTop = resultsOutput.scrollHeight;
    });

    ipcRenderer.on('variable-update', (event, variables) => {
        const varList = document.getElementById('var-list');
        varList.innerHTML = '';
        if (Array.isArray(variables)) {
            variables.forEach(variable => {
                const li = document.createElement('li');
                li.textContent = variable;
                varList.appendChild(li);
            });
        }
    });

    ipcRenderer.on('error', (event, errorMessage) => {
        resultsOutput.textContent += '\n[ERROR] ' + errorMessage + '\n';
        resultsOutput.scrollTop = resultsOutput.scrollHeight;
    });

    commandInput.focus();
});
