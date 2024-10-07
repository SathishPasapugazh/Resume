let loadingMessageElem;

// Function to show loading indicator (bot is "typing")
function showLoading() {
    const chat = document.getElementById("chat");
    loadingMessageElem = document.createElement("div");
    loadingMessageElem.classList.add("message", "loading");
    loadingMessageElem.innerText = "Bot is typing...";  // Show "Bot is typing..." message
    chat.appendChild(loadingMessageElem);
    chat.scrollTop = chat.scrollHeight;
}

// Function to hide loading indicator
function hideLoading() {
    if (loadingMessageElem) {
        loadingMessageElem.remove();  // Remove the typing indicator
        loadingMessageElem = null;
    }
}

// Function to upload resume file
function uploadResume() {
    const formData = new FormData(document.getElementById("resumeForm"));
    fetch("/upload_resume", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        appendMessage(data.response, "bot");
    });
}

// Function to format resume to NC style
function formatToNC() {
    const fileInput = document.getElementById('resumeFile');
    if (fileInput.files.length === 0) {
        alert("Please upload a resume first.");
        return;
    }

    const file = fileInput.files[0];
    const reader = new FileReader();
    reader.onload = function (e) {
        const resumeText = e.target.result;
        showLoading();
        fetch('/format_to_nc', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ resumeText })
        })
        .then(response => response.json())
        .then(data => {
            hideLoading();
            appendMessage(data.response, "bot");
        });
    };
    reader.readAsText(file);
}

// Function to send a message
function sendMessage() {
    const message = document.getElementById("message").value;
    if (message) {
        appendMessage(message, "user");

        // Show loading indicator
        showLoading();

        fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message })
        })
        .then(response => response.json())
        .then(data => {
            hideLoading();  // Hide the loading indicator once the response is received
            appendMessage(data.response, "bot");  // Display the bot's response
        });

        document.getElementById("message").value = "";  // Clear input field
    }
}

// Function to append plain text messages to the chat
function appendMessage(message, type) {
    const chat = document.getElementById("chat");
    const messageElem = document.createElement("div");
    messageElem.classList.add("message");
    messageElem.classList.add(type === "user" ? "user-message" : "bot-message");
    messageElem.innerText = message;
    chat.appendChild(messageElem);
    chat.scrollTop = chat.scrollHeight;
}

// Function to append HTML messages (for bot messages) to the chat
function appendHTMLMessage(message, type) {
    const chat = document.getElementById("chat");
    const messageElem = document.createElement("div");
    messageElem.classList.add("message");
    messageElem.classList.add(type === "user" ? "user-message" : "bot-message");
    messageElem.innerHTML = message;  // Use innerHTML to render HTML content
    chat.appendChild(messageElem);
    chat.scrollTop = chat.scrollHeight;
}

// Event listener to detect Ctrl + Enter for sending message
document.getElementById('message').addEventListener('keydown', function (event) {
    if (event.ctrlKey && event.key === 'Enter') {
        sendMessage();  // Trigger sendMessage when Ctrl + Enter is pressed
    }
});
