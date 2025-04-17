
setInterval(() => {
    fetch("/bookings/bookings/notifications/")
        .then(response => response.json())
        .then(data => {
            let badge = document.getElementById("notification-badge");
            if (data.unread_count > 0) {
                badge.innerText = data.unread_count;
                badge.style.display = "inline";  
            } else {
                badge.style.display = "none";  
            }
        })
        .catch(error => console.error("Error fetching notification count", error));
},5000);