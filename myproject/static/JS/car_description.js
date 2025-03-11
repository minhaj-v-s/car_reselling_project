document.addEventListener("DOMContentLoaded", function () {
    const chatPopup = document.getElementById("chatPopup");
    const openChat = document.getElementById("openChat");
    const closeChatBtn = document.querySelector(".close-chat-btn");
    const chatMessages = document.getElementById("chatMessages");
    const chatInput = document.getElementById("chatInput");
    const sendBtn = document.getElementById("sendBtn");

    let socket = new WebSocket("ws://" + window.location.host + "/ws/chat/");

    // When a message is received from WebSocket
    socket.onmessage = function (event) {
        let messageData = JSON.parse(event.data);
        let messageDiv = document.createElement("div");
        messageDiv.classList.add("message");
        messageDiv.textContent = messageData.message;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight; // Auto-scroll to latest message
    };

    // Send message
    sendBtn.onclick = function () {
        let message = chatInput.value.trim();
        if (message) {
            socket.send(JSON.stringify({ "message": message }));
            chatInput.value = "";
        }
    };

    // Open chat popup
    openChat.addEventListener("click", () => {
        chatPopup.style.display = "block";
    });

    // Close chat popup
    closeChatBtn.addEventListener("click", () => {
        chatPopup.style.display = "none";
    });
});
