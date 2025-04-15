
from django.db import models
from accounts.models import User
from workshops.models import Workshop, Service
import datetime
from django.utils import timezone
from cars.models import Car

class BookingManger(models.Manager):
     def user_booking_validator(self, postData,user=None, instance=None):
           errors = {}

           # Validate appointment_date
           try:
              appointment_date_str = postData.get('appointment_date')
              if not appointment_date_str:
                  errors['appointment_date'] = "Appointment date is required."
              else:
                  # Parse and make timezone-aware
                  naive_appointment_date = datetime.datetime.strptime(
                      appointment_date_str,
                      '%Y-%m-%dT%H:%M'
                  )
                  appointment_date = timezone.make_aware(naive_appointment_date)
                  
                  if appointment_date <= timezone.now():
                      errors['appointment_date'] = "Appointment must be set to a future date and time."

           except ValueError:
               errors['appointment_date'] = "Invalid date format. Please use the date picker."

           # Validate workshop
           if not postData.get('workshop'):
               errors['workshop'] = "Workshop selection is required."

           # Validate service
           if not postData.get('service'):
               errors['service'] = "Service selection is required."

           # Check for overlapping bookings
           workshop = postData.get('workshop')
           if workshop and 'appointment_date' not in errors and appointment_date_str:
               try:
                   appointment_date = datetime.datetime.strptime(
                       appointment_date_str,
                       '%Y-%m-%dT%H:%M'
                   )
                   overlapping_qs = Booking.objects.filter(
                       user_id=user.id,
                       workshop_id=workshop,
                       appointment_date=appointment_date
                   )
                   if instance:
                       overlapping_qs = overlapping_qs.exclude(id=instance.id)

                   if overlapping_qs.exists():
                       errors['appointment_date'] = "You already have a booking at this time in this workshop."
               except ValueError:
                   pass  # Already handled above

           # Service belongs to selected workshop
           if postData.get('workshop') and postData.get('service'):
               try:
                   workshop_instance = Workshop.objects.get(id=postData['workshop'])
                   service_instance = Service.objects.get(id=postData['service'])
                   if service_instance not in workshop_instance.services.all():
                       errors['service'] = "Selected service is not offered by the selected workshop."
               except (Workshop.DoesNotExist, Service.DoesNotExist):
                   errors['workshop'] = "Invalid workshop or service selection."

           return errors

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    objects = BookingManger()

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
