document.getElementById("notifications-btn").addEventListener("click", function () {
    let container = document.getElementById("notifications-container");
    container.style.display = container.style.display === "none" ? "block" : "none";

    fetch("bookings:get_notification")
        .then(response => response.json())
        .then(data => {
            container.innerHTML = ""; 
            if (data.notifications && data.notifications.length > 0) {
                data.notifications.forEach(notification => {
                    let div = document.createElement("div");
                    div.classList.add("notification-item");
                    div.innerText = notification.message;
                    container.appendChild(div);
                });
            } else {
                container.innerHTML = "<p>No Notifications to show </p>";
            }
        })
        .catch(error => console.error('no ontifications to show ' ,error));
});