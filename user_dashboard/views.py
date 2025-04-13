from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
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
import datetime
from django import forms

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
    if request.user.is_authenticated and not (request.user.is_workshop_owner or request.user.is_superuser):
        context = {
            'cars': Car.objects.filter(user=request.user),
            'errors': request.session.pop('errors', None),
            'form_data': request.session.pop('form_data', None),
            'open_modal': request.session.pop('open_modal', False)
        }
        return render(request, 'user_dashboard/my_vehicles.html', context)
    return redirect('landing:main')

def add_vehicle(request):
    if not request.user.is_authenticated or (request.user.is_workshop_owner or request.user.is_superuser):
        return redirect('landing:main')
    
    if request.method == 'POST':
        errors = Car.objects.car_validator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return render(request, 'user_dashboard/my_vehicles.html', {
                'open_modal': True,
                'errors': errors,
                'form_data': request.POST
            })

        Car.objects.create(
            user=request.user,
            make=request.POST['make'],
            model=request.POST['model'],
            year=int(request.POST['year']) if request.POST['year'] else None,
            vin=request.POST['vin']
        )
        messages.success(request, "Vehicle added successfully!")
        return redirect('user_dashboard:vehicles')
    
    return redirect('user_dashboard:vehicles')

def edit_vehicle(request, vehicle_id):
    if not request.user.is_authenticated or (request.user.is_workshop_owner or request.user.is_superuser):
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=401)
    
    try:
        car = Car.objects.get(id=vehicle_id, user=request.user)
    except Car.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Vehicle not found'}, status=404)

    if request.method == 'POST':
        errors = Car.objects.car_validator(request.POST, instance=car)
        
        if errors:
            return JsonResponse({
                'status': 'error',
                'errors': errors
            }, status=400)

        car.make = request.POST['make']
        car.model = request.POST['model']
        car.year = int(request.POST['year']) if request.POST['year'] else None
        car.vin = request.POST['vin']
        car.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Vehicle updated successfully!',
            'redirect': reverse('user_dashboard:vehicles')
        })
    
    # If it's a GET request, return the car data
    return JsonResponse({
        'status': 'success',
        'car': {
            'make': car.make,
            'model': car.model,
            'year': car.year,
            'vin': car.vin
        }
    })

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

