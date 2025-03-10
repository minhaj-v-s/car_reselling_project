document.addEventListener("DOMContentLoaded", function () {
    const chatBtn = document.querySelector('.chat-btn');
    const chatPopup = document.getElementById('chatPopup');
    const closeChatBtn = document.querySelector('.close-chat-btn');
    const chatMessages = document.getElementById('chatMessages');
    const chatInput = document.getElementById('chatInput');
    const sendBtn = document.getElementById('sendBtn');

    // Open Chat Popup
    chatBtn.addEventListener('click', () => {
        chatPopup.style.display = 'block';
    });

    // Close Chat Popup
    closeChatBtn.addEventListener('click', () => {
        chatPopup.style.display = 'none';
    });

    // Send Chat Message
    sendBtn.addEventListener('click', () => {
        const message = chatInput.value.trim();
        if (message) {
            const newMessage = document.createElement('p');
            newMessage.textContent = message;
            chatMessages.appendChild(newMessage);
            chatInput.value = '';
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    });

    // Enter Key to Send Message
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendBtn.click();
        }
    });
});
