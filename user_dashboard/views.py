from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import get_user_model
from django.urls import reverse
from workshops.models import Workshop, Service
from reviews.models import Review
from bookings.models import Booking, Notification
from locations.models import Address
from cars.models import Car
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import JsonResponse
import datetime
from django.utils import timezone

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
    if not request.user.is_authenticated or (request.user.is_workshop_owner or request.user.is_superuser):
        return redirect('landing:main')
    
    vehicle = get_object_or_404(Car, id=vehicle_id, user=request.user)
    if request.method == 'POST':
        vehicle.delete()
        return redirect('user_dashboard:vehicles')
    return redirect('user_dashboard:vehicles')
 
def appointments(request):
    if not request.user.is_authenticated or (request.user.is_workshop_owner or request.user.is_superuser):
        return redirect('landing:main')
    
    # Get upcoming and past appointments
    upcoming_appointments = Booking.objects.filter(
        user=request.user,
        appointment_date__gte=timezone.now()
    ).order_by('appointment_date')
    
    past_appointments = Booking.objects.filter(
        user=request.user,
        appointment_date__lt=timezone.now()
    ).order_by('-appointment_date')
    
    context = {
        'upcoming_appointments': upcoming_appointments,
        'past_appointments': past_appointments,
        'vehicles': Car.objects.filter(user=request.user),
        'workshops': Workshop.objects.all(),
        'form_data': request.session.pop('form_data', None),
        'open_modal': request.session.pop('open_modal', False),
        'errors': request.session.pop('errors', None)
    }

    return render(request, 'user_dashboard/appointments.html', context)

def get_workshop_services(request, workshop_id):
    try:
        services = Service.objects.filter(workshop_id=workshop_id).values('id', 'name', 'price', 'duration')
        return JsonResponse({'status': 'success', 'services': list(services)})
    except Workshop.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Workshop not found'}, status=404)
    
def add_appointment(request):
    if not request.user.is_authenticated or (request.user.is_workshop_owner or request.user.is_superuser):
        return redirect('landing:main')
    
    if request.method == 'POST':        
        errors = Booking.objects.user_booking_validator(request.POST, request.user)
        if errors:
            request.session['errors'] = errors
            #return redirect('user_dashboard:appointments')
            return render(request, 'user_dashboard/appointments.html', {
                'open_modal': True,
                'errors': errors,
                'form_data': request.POST,
                'vehicles': Car.objects.filter(user=request.user),
                'workshops': Workshop.objects.all(),
            })
        
        try:
            workshop = Workshop.objects.get(id=request.POST['workshop'])
            service = Service.objects.get(id=request.POST['service'])
            car = Service.objects.get(id=request.POST['vehicle'])
            
            #TODO: Add Car relationship
            # Create the booking
            booking = Booking.objects.create(
                user=request.user,
                # car=car,
                workshop=workshop,
                service=service,
                appointment_date=request.POST['appointment_date'],
                status='pending'
            )
                
            messages.success(request, "Appointment booked successfully!")
            return redirect('user_dashboard:appointments')
            
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('user_dashboard:appointments')
    
    return redirect('user_dashboard:appointments')


def edit_appointment(request,appointment_id):
    pass


def delete_appointment(request, appointment_id):
    if not request.user.is_authenticated or (request.user.is_workshop_owner or request.user.is_superuser):
        return redirect('landing:main')
    
    if request.method == 'POST':
        booking = get_object_or_404(Booking, id=appointment_id, user=request.user)
        booking.status = 'canceled'
        booking.save()
        return redirect('user_dashboard:appointments')
    return redirect('user_dashboard:appointments')

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

