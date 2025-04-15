document.getElementById("notifications-btn").addEventListener("click", function () {
    let container = document.getElementById("notifications-container");
    
   
    container.style.display = container.style.display === "none" ? "block" : "none";

    fetch("/bookings/bookings/notifications/")  
        .then(response => response.json())
        .then(data => {
            container.innerHTML = "";  

            let badge = document.getElementById("notification-badge");

          
            if (data.unread_count > 0) {
                badge.innerText = data.unread_count;
                badge.style.display = "inline";  
            } else {
                badge.style.display = "none";  
            }
            if (data.notifications && data.notifications.length > 0) {
                data.notifications.forEach(notification => {
                    let div = document.createElement("div");
                    div.classList.add("notification-item");
                    div.innerText = notification.message;
                    container.appendChild(div);
                });
            } else {
                container.innerHTML = "<p>No notifications to show</p>";
            }
        })
        .catch(error => console.error("Error fetching notifications", error));
});


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
}, 30000);