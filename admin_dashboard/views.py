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

# get user model
User = get_user_model()

#Admin Dashboard
def admin_dashboard(request):
    if request.user.is_authenticated and request.user.is_superuser:
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

    return redirect('landing:main')

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
            return redirect('landing:dashboard') 
        
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
            return redirect('landing:dashboard')
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
        image = request.FILES.get('image')

        if address_id:  
            Workshop.objects.create(
                name=name,
                phone=phone,
                address_id=address_id,
                image=image)
            
            return redirect('admin_dashboard:manage_workshops')
        else:
            return HttpResponse("Address is required", status=400)
  
    addresses = Address.objects.all()
    return render(request, 'admin_dashboard/create_workshop.html', {'addresses': addresses})


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
            return JsonResponse({'status': 'deleted'})
        return JsonResponse({'status': 'error'}, status=400)
    return JsonResponse({
            'success': False,
            'error': "Unautorized User",
            'redirect_url': reverse('landing:main')
            })

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
    print("Entered update_service view")
    print("Request method:", request.method)
    print("User:", request.user)

    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            service = get_object_or_404(Service, id=service_id)
            service.name = request.POST.get('name')
            service.price = request.POST.get('price')
            service.description = request.POST.get('description')
            service.duration = request.POST.get('duration')
            service.save()

            print("Service updated successfully")
            return JsonResponse({'success': True})

        print("Request method is not POST")
        return JsonResponse({'success': False, 'error': 'Request method must be POST'}, status=400)

    print("User is not authorized")
    return JsonResponse({
        'success': False,
        'error': "Unauthorized user",
        'redirect_url': reverse('landing:main')
    }, status=403)

