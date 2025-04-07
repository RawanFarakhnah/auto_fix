document.addEventListener('DOMContentLoaded', () => {
    const chatBubble = document.getElementById('chat-bubble');
    const chatBox = document.getElementById('chat-box');
    const sendBtn = document.getElementById('send-btn');
    const userInput = document.getElementById('user-input');
    const messages = document.getElementById('messages');
  
    chatBubble.addEventListener('click', () => {
      chatBox.classList.toggle('hidden');
    });
  
    sendBtn.addEventListener('click', () => {
      const message = userInput.value.trim();
      if (!message) return;
  
      appendMessage('You', message);
      userInput.value = '';
  
      fetch('/chat/',{
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ message })
      })
      .then(res => res.json())
      .then(data => {
        appendMessage('AI', data.reply);
      });
    });
  
    function appendMessage(sender, text) {
      const msg = document.createElement('div');
      msg.classList.add('message');
      msg.classList.add(sender === 'You' ? 'user' : 'ai');
      msg.textContent = text;
      messages.appendChild(msg);
      messages.scrollTop = messages.scrollHeight;
    }
  
    function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }
  });
  function clearText() {
    document.getElementById('messages').textContent = '';
    document.getElementById('user-input').textContent = '';
    const chatBox = document.getElementById('chat-box');
    chatBox.classList.toggle('hidden');
  };
