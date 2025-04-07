document.addEventListener("DOMContentLoaded", function () {
    const chatToggle = document.getElementById("chatToggle");
    const chatBox = document.getElementById("chatBox");
    const chatInput = document.getElementById("chatInput");
    const sendBtn = document.getElementById("sendBtn");
    const messages = document.getElementById("messages");

    chatToggle.addEventListener("click", function () {
        chatBox.classList.toggle("visible");
    });

    sendBtn.addEventListener("click", sendMessage);
    chatInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    });

  


});