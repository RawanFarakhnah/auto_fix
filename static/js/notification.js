document.addEventListener('DOMContentLoaded', function() {
    const notificationBtn = document.getElementById('notifications-btn');
    const badge = document.getElementById('notification-badge');
    
    // Function to update notification count
    function updateNotificationCount() {
        fetch("/bookings/bookings/notifications/")
            .then(response => response.json())
            .then(data => {
                if (data.unread_count > 0) {
                    badge.textContent = data.unread_count > 9 ? '9+' : data.unread_count;
                    badge.style.display = 'inline-block';
                    badge.classList.add('new-notification');
                    setTimeout(() => badge.classList.remove('new-notification'), 1000);
                } else {
                    badge.style.display = 'none';
                }
            })
            .catch(error => console.error("Error:", error));
    }
    
    // Check for new notifications every 30 seconds
    updateNotificationCount(); // Initial check
    setInterval(updateNotificationCount, 30000);
});