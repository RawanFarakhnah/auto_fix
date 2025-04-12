from django.db.models import Count, Q
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import get_user_model
from django.urls import reverse
from workshops.models import Workshop, Service
from reviews.models import Review
from bookings.models import Booking, Notification
from locations.models import Address
from cars.models import Car
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from workshops.models import Address,Service
import datetime

# get user model
User = get_user_model()

#user Dashbord
def user_dashboard(request):
    if request.user.is_authenticated and not ( request.user.is_workshop_owner or request.user.is_superuser ):        
        #Get upcoming appointments (next 30 days)
        upcoming_appointments = Booking.objects.filter(
           user=request.user,
           appointment_date__gte=datetime.date.today(),
           appointment_date__lte=datetime.date.today() + datetime.timedelta(days=30),
        ).order_by('appointment_date')[:5]
                
        # Get recent notifications
        recent_notifications = Notification.objects.filter(
           user=request.user,
        ).order_by('-created_at')[:5]

        # Get user's cars
        user_cars = Car.objects.filter(user=request.user)

        # Get nearby workshops (simplified - would use geolocation in production)
        nearby_workshops = Workshop.objects.all()[:3]
        
        # Count stats for dashboard cards
        stats = {
            'upcoming_appointments': Booking.objects.filter(
                user=request.user,
                appointment_date__gte=datetime.date.today(),
                status__in=['pending', 'confirmed']
             ).count(),
             'active_vehicles': user_cars.count(),
             'pending_services': 0,  # This would come from maintenance reminders
             'unread_notifications': Notification.objects.filter(
                user=request.user,
                is_read=False
              ).count()
        }
        
        context = {
            'upcoming_appointments': upcoming_appointments,
            'recent_notifications': recent_notifications,
            'user_cars': user_cars,
            'nearby_workshops': nearby_workshops,
            'stats': stats,
        } 
        
        return render(request, 'user_dashboard/dashboard.html', context)
       
    return redirect('landing:main')


def profile(request):
    if request.user.is_authenticated and not ( request.user.is_workshop_owner or request.user.is_superuser ):        
        return render(request, 'user_dashboard/my_profile.html')

    return redirect('landing:main')

def vehicles(request):
    if request.user.is_authenticated and not ( request.user.is_workshop_owner or request.user.is_superuser ):        
        context = {
            'cars': Car.objects.filter(user=request.user) 
        }
        return render(request, 'user_dashboard/my_vehicles.html', context)

    return redirect('landing:main')

def add_vehicle(request):
    if request.user.is_authenticated and not ( request.user.is_workshop_owner or request.user.is_superuser ):        
       if request.method == "POST":
        make = request.POST.get("make")
        model = request.POST.get("model")
        year = request.POST.get("year")
        vin = request.POST.get("vin")

        errors = {}

        if Car.objects.filter(vin=vin).exists():
            errors['vin'] = 'A car with this VIN already exists.'
            messages.error(request, errors)
            return redirect('user_dashboard:vehicles')
            
        Car.objects.create(
            user=request.user,
            make=make,
            model=model,
            year=year,
            vin=vin
        )
        messages.success(request, "Vehicle added successfully!")
        return redirect('user_dashboard:vehicles')
    return redirect('landing:main')

def edit_vehicle(request,vehicle_id):
    pass

def delete_vehicle(request,vehicle_id):
    pass

def appointments(request):
    if request.user.is_authenticated and not ( request.user.is_workshop_owner or request.user.is_superuser ):        
        return render(request, 'user_dashboard/appointments.html')

    return redirect('landing:main')


def services(request):
    if request.user.is_authenticated and not ( request.user.is_workshop_owner or request.user.is_superuser ):        
        return render(request, 'user_dashboard/services.html')

    return redirect('landing:main')


def notifications(request):
    if request.user.is_authenticated and not ( request.user.is_workshop_owner or request.user.is_superuser ):        
        return render(request, 'user_dashboard/notifications.html')

    return redirect('landing:main')

@csrf_exempt
def mark_notification_as_read(request, notification_id):
    if request.user.is_authenticated and not ( request.user.is_workshop_owner or request.user.is_superuser ):        
       if request.method == 'POST':
          try:
              notification = Notification.objects.get(
                  id=notification_id,
                  user=request.user
              )
              notification.is_read = True
              notification.save()
              return JsonResponse({'success': True})
          except Notification.DoesNotExist:
              return JsonResponse({'success': False, 'error': 'Notification not found'}, status=404)
       return redirect('user_dashboard:notifications')
    return redirect('landing:main')

def reviews(request):
    if request.user.is_authenticated and not ( request.user.is_workshop_owner or request.user.is_superuser ):        
        return render(request, 'user_dashboard/reviews.html')

    return redirect('landing:main')

