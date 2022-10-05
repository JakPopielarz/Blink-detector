let textarea = document.getElementById('keybind'),
consoleLog = document.getElementById('console-log'),
btnReset = document.getElementById('btn-capture'),
capturing = false;

function logMessage(message) {
  consoleLog.innerHTML += `${message}<br>`;
}

function clearMessages() {
    let child = consoleLog.firstChild;
    while (child) {
        consoleLog.removeChild(child);
        child = consoleLog.firstChild;
    }
}

textarea.addEventListener('keyup', (e) => {
    if (capturing) {
        clearMessages();
        logMessage(`Key "${textarea.value}" captured`);
        capturing = !capturing;
    }
});

btnReset.addEventListener('click', (e) => {
    if (capturing) return;

    clearMessages();
    logMessage(`Now capturing the keybind`);
    textarea.value = '';
    capturing = true;
});
