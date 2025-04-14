from django.db import models
from accounts.models import User
from workshops.models import Workshop, Service

class ReviewManager(models.Manager):
    def validate_review(self, user, workshop, service):
        """
        Validates if a user can review a service at a workshop
        Returns a dictionary of errors if validation fails
        """
        errors = {}
        
        if self.filter(user=user, workshop=workshop, service=service).exists():
            errors['reviewed'] = "You've already reviewed this service at this workshop"
        
        return errors

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    response = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = ReviewManager()
    class Meta:
        unique_together = ('user', 'workshop', 'service') #Prevents Multiple Reviews
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.rating}★ by {self.user}"