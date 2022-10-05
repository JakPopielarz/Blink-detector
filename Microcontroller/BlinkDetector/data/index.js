let textarea = document.getElementById('keybind'),
consoleLog = document.getElementById('console-log'),
btnReset = document.getElementById('btn-capture'),
capturing = false;

function logMessage(message) {
    let child = consoleLog.firstChild;
    while (child) {
        consoleLog.removeChild(child);
        child = consoleLog.firstChild;
    }
  consoleLog.innerHTML += `${message}<br>`;
}

function clearMessages() {
    let child = consoleLog.firstChild;
    while (child) {
        consoleLog.removeChild(child);
        child = consoleLog.firstChild;
    }
}

window.addEventListener('keydown', function (e) {
    if (capturing && e.key == "Enter"){
        clearMessages();
        logMessage(`You pressed ${e.key}`);

        textarea.value = e.key;
        capturing = !capturing;
    }
}, false);

window.addEventListener('keyup', function (e) {
    if (capturing) {
        clearMessages();
        logMessage(`You pressed ${e.key}`);
    
        textarea.value = e.key;
        capturing = !capturing;
    }
  }, false);

btnReset.addEventListener('click', (e) => {
    if (capturing) return;

    clearMessages();
    logMessage(`Now capturing the keybind`);
    textarea.value = '';
    capturing = true;
});
