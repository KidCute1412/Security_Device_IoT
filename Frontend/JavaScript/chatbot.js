function toggleChatBot() {
    const chatbot = document.getElementById('chat-bot');
    if (chatbot.style.display === 'none') {
        chatbot.style.display = 'block';
    } else {
        chatbot.style.display = 'none';
    }
}

//  Send a message to the chat bot and display like a chat bubble
function sendMessage() {
    const input = document.getElementById('user-input-chatbot');
    const message = input.value.trim();
    if (!message) return; // Do not send empty messages
    appendMessage(message, "user");
    input.value = ''; // Clear the input field

    // Call the chat bot API 

    fetch("http://localhost:5000/api/chat-bot", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "OKE") {
            appendMessage(data.response, "bot");
        } else {
            appendMessage("Error: " + data.message, "bot");
        }
    }
    )
    .catch(error => {
        console.error("Error:", error);
        appendMessage("Error: Unable to connect to the chat bot.", "bot");
    }
    );
}


function appendMessage(msg, type) {
    const chatBox = document.getElementById("chat-bot-content");

    const msgDiv = document.createElement("div");
    if (type === "bot") {
        msgDiv.className = "chat-bot-message";
    } else {
        msgDiv.className = "user-chat-message";
    }


    const span = document.createElement("span");
    span.className = type === "bot" ? "bot-message" : "user-message";
    span.innerText = msg;

    msgDiv.appendChild(span);
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}