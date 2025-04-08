
from django.db import models
from accounts.models import User
from workshops.models import Workshop, Service


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-appointment_date']

    def __str__(self):
        return f"Booking by {self.user} at {self.workshop} for {self.service} on {self.appointment_date}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)  # Short message for the notification
    is_read = models.BooleanField(default=False)  # Whether the user has read the notification
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when created   
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='notifications')  # Link to a booking


    class Meta:
        ordering = ['-created_at']  # Order by newest first

    def __str__(self):
        return f"Notification for {self.user} - {self.message[:50]}"  # Displaying first 50 chars of message
