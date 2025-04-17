from django.db.models import Count, Q
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import get_user_model
from django.urls import reverse
from workshops.models import Workshop, Service
from bookings.models import Booking
from locations.models import Address
from cars.models import Car
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from django.utils.timezone import now, timedelta
from bookings.models import Booking, Notification
from django.contrib.auth import update_session_auth_hash

# get user model
User = get_user_model()

#Admin Dashboard
def admin_dashboard(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
       return redirect('landing:main')
    
    last_30_days = timezone.now() - timedelta(days=30)

    bookings_by_day = Booking.objects.filter(appointment_date__gte=last_30_days) \
    .values('appointment_date__date') \
    .annotate(count=Count('id')) \
    .order_by('appointment_date__date')
    
    dates = [b['appointment_date__date'].strftime('%Y-%m-%d') for b in bookings_by_day]  
    counts = [b['count'] for b in bookings_by_day]  

    users_growth_by_day = User.objects.filter(date_joined__gte=last_30_days) \
      .values('date_joined__date') \
      .annotate(count=Count('id')) \
      .order_by('date_joined__date')

    userGrowth_dates = [b['date_joined__date'].strftime('%Y-%m-%d') for b in users_growth_by_day]  
    userGrowth_counts = [b['count'] for b in users_growth_by_day]  

    context = {
       'userGrowth_dates': userGrowth_dates,
       'userGrowth_counts': userGrowth_counts,
       'dates': dates,
       'counts': counts,
       'users_count': User.objects.count(),
       'active_workshops': Workshop.objects.count(),
       'pending_bookings': Booking.objects.filter(status='pending').count(),
       'completed_bookings': Booking.objects.filter(status='completed').count(),
       }
    
    return render(request, 'admin_dashboard/dashboard.html', context)

def profile(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
       return redirect('landing:main')
    
    return render(request, 'admin_dashboard/my_profile.html')


def profile_update(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
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

    return redirect('admin_dashboard:profile')
  
def update_address(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('landing:main')

    if request.method != 'POST':
         return redirect('admin_dashboard:profile')

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
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('landing:main')

    if request.method != 'POST':
         return redirect('admin_dashboard:profile')
    
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

def create_user(request):
    if request.user.is_authenticated and request.user.is_superuser:    
        if request.method == 'POST':
            errors = User.objects.register_validator(request.POST)          
            
            if errors:
                return render(request, 'admin_dashboard/create_user.html', {'errors': errors, 'postData': request.POST})
                        
            role = request.POST.get('role')
            is_superuser = False
            is_workshop_owner = False

            if role == 'admin':
              is_superuser = True
            elif role == 'workshop':
              is_workshop_owner = True
              # else: regular user — no extra flags

            user = User.objects.create(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['email'],
                phone=request.POST.get('phone', ''),
                password=make_password(request.POST['password']),
                is_superuser=is_superuser,
                is_workshop_owner=is_workshop_owner,
            )
            
            messages.success(request, "User created successfully")
            return redirect('admin_dashboard:manage_users')
        
        return render(request, 'admin_dashboard/create_user.html')

def edit_user(request, user_id):
    if request.user.is_authenticated and request.user.is_superuser:
        try:
            user = User.objects.get(id=user_id)
            # Pass role data to the template

            role = 'user'
            if user.is_superuser:
                role = 'admin'
            elif user.is_workshop_owner:
                role = 'workshop'
            
            return render(request, 'admin_dashboard/update_user.html', {
                'user_obj': user,
                'role': role,  # Ensure this is passed for role selection in the form
            })
        except User.DoesNotExist:
            return redirect('admin_dashboard:manage_users')
    return redirect('landing:main')

@csrf_exempt
def update_user(request, user_id):
    if request.method == "POST":
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User not found'})
        
        role = request.POST.get('role')
        is_superuser = False
        is_workshop_owner = False

        if role == 'admin':
            is_superuser = True
        elif role == 'workshop':
            is_workshop_owner = True

        # Update user attributes
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone', '')  # Default to empty string if no phone provided
        
        # Set role-related flags
        user.is_superuser = is_superuser
        user.is_workshop_owner = is_workshop_owner
        
        user.save()

        return JsonResponse({
            'success': True,
            'user_id': user.id,
            'full_name': user.get_full_name(),
            'email': user.email,
            'redirect_url': reverse('admin_dashboard:manage_users')
        })

    return JsonResponse({
       'success': True,
       'message': "User updated successfully",
       'redirect_url': reverse('landing:dashboard')
    })

@csrf_exempt
def delete_user(request, user_id):
    if request.user.is_authenticated and request.user.is_superuser:
 
        if request.method == "POST":
            user = User.objects.get(id=user_id)
            user.delete()
            
            return JsonResponse({
             'success': True,
            })
        
        return JsonResponse({
        'success': False,
        'error':"User Delete Faild"
        })

    return JsonResponse({
        'success': False,
        'error': "Unautorized User",
        'redirect_url': reverse('landing:main')
        })

def manage_users(request):
    if not request.user.is_superuser:
        return redirect('landing:main')

    users = User.objects.all().order_by('-date_joined')
    
    role = request.GET.get('role', '')
    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')

    if role:
        if role == 'admin':
           users = users.filter(is_superuser=True)
        elif role == 'owner':
           users = users.filter(is_workshop_owner=True)
        elif role == 'user':
           users = users.filter(is_superuser=False,is_workshop_owner=False)
           
    if from_date:
        users = users.filter(date_joined__gte=from_date)
    if to_date:
        users = users.filter(date_joined__lte=to_date)

    context = {
        'all_users': users,
    }

    return render(request, 'admin_dashboard/manage_users.html', context)

def manage_workshops(request):
    workshops = Workshop.objects.all()
    return render(request, 'admin_dashboard/manage_workshops.html', {'workshops': workshops})
  


def create_workshop(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address_id = request.POST.get('address_id')
        owner_id = request.POST.get('owner_id') 
        image = request.FILES.get('image')

        if address_id and owner_id:  
            Workshop.objects.create(
                name=name,
                phone=phone,
                address_id=address_id,
                owner_id=owner_id,
                image=image)
            
            return redirect('admin_dashboard:manage_workshops')
        else:
            return HttpResponse("Address and Owner are required", status=400)

    addresses = Address.objects.all()
    owners = User.objects.filter(is_workshop_owner=True)
  
    return render(request, 'admin_dashboard/create_workshop.html', {
        'addresses': addresses,
        'owners': owners
    })

from django.db.models import Q

def edit_workshop(request, id):
    workshop = Workshop.objects.get(id=id)
    addresses = Address.objects.all()
    
    owners = User.objects.filter(
        is_workshop_owner=True,
        workshop__isnull=True  
    )

    return render(request, 'admin_dashboard/update_workshop.html', {
        'workshop': workshop,
        'addresses': addresses,
        'owners': owners 
    })


@csrf_exempt
def workshop_update(request, id):
    if request.method == 'POST':
        try:
            workshop = Workshop.objects.get(id=id)
        except Workshop.DoesNotExist:
            return JsonResponse({'error': 'Workshop not found'}, status=404)

        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address_id = request.POST.get('address_id')
        owner_id = request.POST.get('owner_id') 
        image = request.FILES.get('image')

        if name:
            workshop.name = name
        if phone:
            workshop.phone = phone
        if address_id:
            workshop.address_id = address_id
        if image:
            workshop.image = image
        if owner_id:
            try:
                owner = User.objects.get(id=owner_id)
                workshop.owner = owner
            except User.DoesNotExist:
                return JsonResponse({'error': 'Owner not found'}, status=404)

        workshop.save()
        return JsonResponse({
            'status': 'updated',
            'name': name,
            'phone': phone,
            'owner_id': owner_id
        })

    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def delete_workshop(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            try:
                workshop = Workshop.objects.get(id=id)
                workshop.delete() 
                return JsonResponse({'status': 'deleted'})
            except Workshop.DoesNotExist:
                return JsonResponse({'error': 'Workshop not found'}, status=404)
        return JsonResponse({'error': 'Invalid request'}, status=400)
    return JsonResponse({
            'success': False,
            'error': "Unautorized User",
            'redirect_url': reverse('landing:main')
            })

def manage_services(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('landing:main')
    
    services = Service.objects.all()
    return render(request, 'admin_dashboard/manage_services.html', {'services': services}) 

def create_service(request):
    if not request.user.is_superuser:
        return redirect('landing:main')
    
    if request.method == 'GET':
        workshops = Workshop.objects.all()
        return render(request, 'admin_dashboard/create_service.html', {'workshops': workshops})

    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        description = request.POST['description']
        duration = request.POST['duration']
        workshop_id = request.POST['workshop_id']

        try:
            workshop = Workshop.objects.get(id=workshop_id)
            Service.objects.create(
                name=name,
                price=price,
                description=description,
                duration=duration,
                workshop=workshop
            )
        except Workshop.DoesNotExist:
            
            return render(request, 'admin_dashboard/create_service.html', {
                'workshops': Workshop.objects.all(),
                'error': 'Workshop not found.'
            })

        return redirect('admin_dashboard:manage_services') 
      


@csrf_exempt
def delete_service(request, service_id):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            service = get_object_or_404(Service, id=service_id)
            service.delete()
            
            return redirect('admin_dashboard:manage_services')
        return redirect('admin_dashboard:manage_services')
    

def edit_service(request, service_id):
    
    if request.user.is_authenticated and request.user.is_superuser:
        service = get_object_or_404(Service, id=service_id)
        context = {
            'service': service
        }
        return render(request, 'admin_dashboard/update_service.html', context)
    return JsonResponse({
            'success': False,
            'error': "Unautorized User",
            'redirect_url': reverse('landing:main')
            })     


@csrf_exempt
def update_service(request, service_id):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            service = get_object_or_404(Service, id=service_id)
            service.name = request.POST.get('name')
            service.price = request.POST.get('price')
            service.description = request.POST.get('description')
            service.duration = request.POST.get('duration')
            service.save()

            return JsonResponse({'success': True})

        return JsonResponse({'success': False, 'error': 'Request method must be POST'}, status=400)

    return JsonResponse({
        'success': False,
        'error': "Unauthorized user",
        'redirect_url': reverse('landing:main')
    }, status=403)


def notifications(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('landing:main')
    
    all_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')

    # Paginate with 5 notifications per page
    paginator = Paginator(all_notifications, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'notifications': page_obj,
    }

    return render(request, 'admin_dashboard/notifications.html', context)

@csrf_exempt
def mark_notification_as_read(request, notification_id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('landing:main')
     
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
    return redirect('admin_dashboard:notifications')
  

def mark_all_notifications_as_read(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
      return redirect('landing:main')
   
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return JsonResponse({'status': 'success'})
