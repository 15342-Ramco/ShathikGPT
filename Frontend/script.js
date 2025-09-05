const messagesDiv = document.getElementById('messages');

async function sendMessage() {
    const inputBox = document.getElementById('user-input');
    const text = inputBox.value.trim();
    if (!text) return;

    addMessage(text, 'user');
    inputBox.value = '';

    const loadingId = addMessage("Dude! is typing...", 'bot', true);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;

    try {
        const response = await fetch("https://shathikgpt.onrender.com/generate", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({text: text})
        });
        const data = await response.json();
        updateMessage(loadingId, data.generated_text);

    } catch (err) {
        updateMessage(loadingId, "Error: could not generate response.");
    }
}

function addMessage(text, type, isLoading=false) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${type}`;
    if (isLoading) msgDiv.style.fontStyle = "italic";
    msgDiv.innerText = text;
    messagesDiv.appendChild(msgDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
    return msgDiv;
}

function updateMessage(msgDiv, text) {
    msgDiv.innerText = text;
    msgDiv.style.fontStyle = "normal";
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}
