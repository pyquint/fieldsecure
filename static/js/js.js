function encryptMessage() {
    const message = document.getElementById('message').value;
    const output = document.getElementById('output');

    if (!message) {
        output.textContent = "Please enter a message.";
        return;
    }

    // Simple encryption logic (for demonstration purposes only)
    const encrypted = message.split('').map(char => char.charCodeAt(0) + 1).join(' ');
    output.textContent = `${encrypted}`;
}

function decryptMessage() {
    const message = document.getElementById('message').value;
    const output = document.getElementById('output');

    if (!message) {
        output.textContent = "Please enter a message.";
        return;
    }

    // Simple decryption logic (for demonstration purposes only)
    const decrypted = message.split(' ').map(char => String.fromCharCode(char - 1)).join('');
    output.textContent = ` ${decrypted}`;
}

