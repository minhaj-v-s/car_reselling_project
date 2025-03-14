document.addEventListener("DOMContentLoaded", function () {
    const chatPopup = document.getElementById("chatPopup");
    const openChat = document.getElementById("openChat");
    const closeChatBtn = document.querySelector(".close-chat-btn");
    const chatMessages = document.getElementById("chatMessages");
    const chatInput = document.getElementById("chatInput");
    const sendBtn = document.getElementById("sendBtn");

    let socket = new WebSocket("ws://" + window.location.host + "/ws/chat/");

    // Function to append messages
    function appendMessage(message, sender) {
        let messageDiv = document.createElement("div");
        messageDiv.classList.add("message", sender);
        messageDiv.textContent = message;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Receiving messages
    socket.onmessage = function (event) {
        let messageData = JSON.parse(event.data);
        appendMessage(messageData.message, "dealer");
    };

    // Sending messages
    sendBtn.onclick = function () {
        let message = chatInput.value.trim();
        if (message) {
            socket.send(JSON.stringify({ "message": message }));
            appendMessage(message, "user");
            chatInput.value = "";
        }
    };

    chatInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            sendBtn.click();
        }
    });

    // Open and close chat popup
    openChat.addEventListener("click", () => {
        chatPopup.style.display = "block";
    });

    closeChatBtn.addEventListener("click", () => {
        chatPopup.style.display = "none";
    });
});

const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/chat/' + receiverUsername + '/');
    
        chatSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            const messageElement = document.createElement('div');
            messageElement.innerHTML = `<b>${data.sender}:</b> ${data.message}`;
            document.getElementById('chat-messages').appendChild(messageElement);
        };

        
        document.getElementById('send-btn').onclick = function() {
            console.log("Sender Email:", senderUsername); 
            const messageInput = document.getElementById('message-input');
            const message = messageInput.value;
            chatSocket.send(JSON.stringify({
                'message': message,
                'sender': senderUsername  // Dynamically set this
            }));
            messageInput.value = '';
        };
