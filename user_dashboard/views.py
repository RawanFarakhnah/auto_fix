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
import datetime
from django.utils import timezone
from django.core.paginator import Paginator
from django.utils.timezone import make_naive
from django.db.models import Avg
from django.contrib.auth import update_session_auth_hash


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


def profile_update(request):
    if not (request.user.is_authenticated and not ( request.user.is_workshop_owner or request.user.is_superuser)):
        return redirect('landing:main')

    if request.method == 'POST':
        user = request.user
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()

        errors = []

        # Validate first name
        if not first_name:
            errors.append("First name is required.")
        elif len(first_name) > 30:
            errors.append("First name cannot exceed 30 characters.")
        else:
            user.first_name = first_name

        # Validate last name
        if not last_name:
            errors.append("Last name is required.")
        elif len(last_name) > 30:
            errors.append("Last name cannot exceed 30 characters.")
        else:
            user.last_name = last_name

        # Validate email
        if not email:
            errors.append("Email is required.")
        elif '@' not in email:
            errors.append("Enter a valid email address.")
        elif User.objects.exclude(id=user.id).filter(email=email).exists():
            errors.append("Email is already in use by another account.")
        else:
            user.email = email

        # Validate phone
        if not phone:
            errors.append("Phone number is required.")
        elif not phone.isdigit():
            errors.append("Phone number must contain only digits.")
        elif len(phone) != 10:
            errors.append("Phone number must be 10 digits.")
        elif not phone.startswith("05"):
            errors.append("Phone number must start with 05.")
        elif User.objects.exclude(id=user.id).filter(phone=phone).exists():
            errors.append("Phone number is already used by another user.")
        else:
            user.phone = phone

        if errors:
            return JsonResponse({
                'status': 'error',
                'errors': errors
            })

        try:
            user.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Profile updated successfully!'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'errors': ['Failed to update profile. Please try again.']
            }, status=500)

    return redirect('user_dashboard:profile')
  
def update_address(request):
    if not (request.user.is_authenticated and not ( request.user.is_workshop_owner or request.user.is_superuser)):
        return redirect('landing:main')

    if request.method != 'POST':
         return redirect('user_dashboard:profile')

    user = request.user
    street = request.POST.get('street', '').strip()
    city = request.POST.get('city', '').strip()
    region = request.POST.get('region', '').strip()
    country = request.POST.get('country', '').strip()
    postal_code = request.POST.get('postal_code', '').strip()
    latitude = request.POST.get('latitude', '').strip() or None
    longitude = request.POST.get('longitude', '').strip() or None

    # Validate required fields
    if not all([street, city, country]):
        return JsonResponse({
            'status': 'error',
            'errors': ['Street, City and Country are required fields.']
        })

    try:
        if latitude is not None:
            latitude = float(latitude)
            if not (-90 <= latitude <= 90):
                raise ValueError("Latitude must be between -90 and 90")
        
        if longitude is not None:
            longitude = float(longitude)
            if not (-180 <= longitude <= 180):
                raise ValueError("Longitude must be between -180 and 180")

        if user.address:
            address = user.address
        else:
            address = Address()
            user.address = address

        address.street = street
        address.city = city
        address.region = region
        address.country = country
        address.postal_code = postal_code
        address.latitude = latitude
        address.longitude = longitude

        address.save()
        user.save()

        return JsonResponse({'status': 'success'})
    
    except ValueError as e:
        return JsonResponse({'status': 'error', 'errors': [str(e)]}, status=400)
    
    except Exception as e:
        return JsonResponse({'status': 'error', 'errors': [f"Error saving address: {str(e)}"]}, status=500)

def change_password(request):
    if not (request.user.is_authenticated and not ( request.user.is_workshop_owner or request.user.is_superuser)):
        return redirect('landing:main')

    if request.method != 'POST':
         return redirect('user_dashboard:profile')
    
    errors = []
    
    current_password = request.POST.get('current_password')
    new_password = request.POST.get('new_password')
    confirm_password = request.POST.get('confirm_password')

    if not request.user.check_password(current_password):
        errors.append( "Current password is incorrect.")
        
    if len(new_password) < 8:
        errors.append("New password must be at least 8 characters long.")
        
    if new_password != confirm_password:
        errors.append("New password and confirmation do not match.")
     
    if errors:
       return JsonResponse({
           'status': 'error',
           'errors': errors
       })
    
    request.user.set_password(new_password)
    request.user.save()
    update_session_auth_hash(request, request.user)  # Keeps user logged in after password change
    
    return JsonResponse({'status': 'success'})

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
       appointment_date__lt=make_naive(timezone.now())
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
            upcoming_appointments = Booking.objects.filter(
                user=request.user,
                appointment_date__gte=timezone.now()
                ).order_by('appointment_date')
            
            past_appointments = Booking.objects.filter(
                user=request.user,
                appointment_date__lt=make_naive(timezone.now())
                ).order_by('-appointment_date')
            return render(request, 'user_dashboard/appointments.html', {
                'open_modal': True,
                'upcoming_appointments': upcoming_appointments,
                'past_appointments': past_appointments,
                'errors': errors,
                'form_data': request.POST,
                'vehicles': Car.objects.filter(user=request.user),
                'workshops': Workshop.objects.all(),
            })
        
        try:
            workshop = Workshop.objects.get(id=request.POST['workshop'])
            service = Service.objects.get(id=request.POST['service'])
            car = Car.objects.get(id=request.POST['vehicle'])
           
            # Create the booking
            booking = Booking.objects.create(
                user=request.user,
                car=car,
                workshop=workshop,
                service=service,
                appointment_date=request.POST['appointment_date'],
                status='pending'
            )
        
            # Create notification for the user
            Notification.objects.create(
                user=request.user,
                message=f"Your appointment at {workshop.name} for {service.name} is submitted and is now pending.",
                booking=booking
            )

            # Create notification for the workshop owner
            if hasattr(workshop, 'owner'):
                Notification.objects.create(
                    user=workshop.owner,
                    message=f"You have a new appointment from {request.user.get_full_name()} for {service.name}.",
                    booking=booking
            )
                
            messages.success(request, "Appointment booked successfully!")
            return redirect('user_dashboard:appointments')
            
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('user_dashboard:appointments')
    
    return redirect('user_dashboard:appointments')

def appointment_details(request, appointment_id):
    if not request.user.is_authenticated or (request.user.is_workshop_owner or request.user.is_superuser):
        return redirect('landing:main')
    booking = get_object_or_404(Booking, id=appointment_id, user=request.user)
    
    data = {
        "date": booking.appointment_date.strftime("%b %d, %Y %H:%M"),
        "workshop": booking.workshop.name,
        "service": booking.service.name,
        "vehicle": booking.car.__str__(),
        "status": booking.get_status_display(),
        "notes": booking.notes if hasattr(booking, "notes") else "No notes available."
    }
    return JsonResponse(data)

@csrf_exempt
def delete_appointment(request, appointment_id):
    if not request.user.is_authenticated and not ( request.user.is_workshop_owner or request.user.is_superuser ):
      return redirect('landing:main')  
   
    booking = get_object_or_404(Booking, id=appointment_id, user=request.user)
    if request.method == 'POST':
        booking.status = 'canceled'
        booking.save()

         # Notify the user (who canceled the appointment)
        Notification.objects.create(
            user=request.user,
            message=f"Your appointment with the workshop '{booking.workshop.name}' has been canceled.",
            booking=booking
        )

        # Notify the workshop owner
        workshop_owner = booking.workshop.owner  # Adjust this line if the workshop's owner field has a different name
        Notification.objects.create(
            user=workshop_owner,
            message=f"The user {request.user.username} has canceled their booking.",
            booking=booking
        )

    return JsonResponse({
        'status': 'success', 
        'redirect_url': reverse('user_dashboard:appointments')
        })

def services(request):
    if not request.user.is_authenticated and not ( request.user.is_workshop_owner or request.user.is_superuser ):        
        return redirect('landing:main')
    
    # Get all completed bookings for this user
    current_user = User.objects.get(id = request.user.id)
    region = getattr(request.user.address, 'region', None)
    completed_bookings = Booking.objects.filter(user=request.user, status='completed').select_related('workshop', 'service')
    recomended_service = Service.objects.filter(
        workshop__address__region__iexact=region
        )[:3]

    if recomended_service.exists():
        recomended_service = recomended_service
    else:
        top_rated_services = (
            Service.objects.annotate(avg_rating=Avg('review__rating'))
            .order_by('-avg_rating')[:3]
        )
        recomended_service = top_rated_services

    context = {
        'bookings_service_history': completed_bookings,
        'recomended_services':recomended_service
    }

    return render(request, 'user_dashboard/services.html', context)


def services_details(request, service_id):
    if not request.user.is_authenticated and not ( request.user.is_workshop_owner or request.user.is_superuser ):        
        return redirect('landing:main')
    
    try:
        service = Service.objects.get(id=service_id)
        data = {
            "name": service.name,
            "description": service.description,
            "price": service.price,
            "workshop": service.workshop.name if service.workshop else "Unknown",
        }
        return JsonResponse(data)
    except Service.DoesNotExist:
        return JsonResponse({'error': 'Service not found'}, status=404)




def notifications(request):
    if not request.user.is_authenticated and not (request.user.is_workshop_owner or request.user.is_superuser):        
        return redirect('landing:main')
    all_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(all_notifications, 5)

    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number)  

    context = {
        'notifications': page_obj.object_list,  
        'page_obj': page_obj, 
    }

    return render(request, 'user_dashboard/notifications.html', context)

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

def mark_all_notifications_as_read(request):
    if not request.user.is_authenticated and not ( request.user.is_workshop_owner or request.user.is_superuser ):
      return redirect('landing:main')  
   
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return JsonResponse({'status': 'success'})

def reviews(request):
    if not request.user.is_authenticated and not (request.user.is_workshop_owner or request.user.is_superuser):        
        return redirect('landing:main')

    reviews = Review.objects.filter(user = request.user.id)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and 'workshop_id' in request.GET:
        workshop_id = request.GET.get('workshop_id')
        services = Service.objects.filter(workshop_id=workshop_id).values('id', 'name')
        return JsonResponse({'services': list(services)})

 
    workshops = Workshop.objects.all()
    return render(request, 'user_dashboard/reviews.html', {'workshops': workshops,'reviews':reviews})

@csrf_exempt
def add_review(request):
    if not request.user.is_authenticated and not (request.user.is_workshop_owner or request.user.is_superuser):        
        return redirect('landing:main')
    if request.method == "POST":
        print("POST DATA:", request.POST)
        try:
            workshop_id = request.POST.get("workshop")
            service_id = request.POST.get("service")
            rating = int(request.POST.get("rating", 0))
            comment = request.POST.get("comment")

            workshop = Workshop.objects.get(id=workshop_id)
            service = Service.objects.get(id=service_id)

            review,created = Review.objects.get_or_create(
                user=request.user,
                workshop=workshop,
                service=service,
                defaults={'rating': rating, 'comment': comment}
            )
            notification = Notification.objects.create(
                user = request.user ,
                message = f"{request.user} have been review {service.name}",
                booking = Booking.objects.filter(service = service).first()
            )
            if not created:
                return JsonResponse({'status': 'error', 'message': 'You already reviewed this service.'})

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def delete_review(request):
    if request.method == "POST":
        review_id = request.POST.get("id")

        try:
            review = Review.objects.get(id=review_id, user=request.user)
            review.delete()
            return JsonResponse({'status': 'success'})
        except Review.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Review not found.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})
