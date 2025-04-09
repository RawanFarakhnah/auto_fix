from django.db.models import Count, Q
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import get_user_model
from django.urls import reverse
from workshops.models import Workshop, Service
from reviews.models import Review
from bookings.models import Booking
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



# Create your views here.
User = get_user_model()

def main(request):
    if request.user.is_authenticated:
        return redirect('landing:dashbord')

    return render(request, 'landing\main.html')

def contact(request):
    return render(request, 'landing\contact.html')

def dashbord(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('landing:admin_dashboard')
        elif request.user.is_workshop_owner:
            return redirect('landing:owner_dashboard')
        else:
            return redirect('landing:user_dashboard')
    else:
        return redirect('landing:login')
    
#Admin Dashbord
def user_dashboard(request):
    return render(request, 'user_dashboard/dashboard.html')

#Admin Dashbord
def owner_dashboard(request):
    context = {
        'users_count': User.objects.count(),
        'pending_bookings': Booking.objects.filter(status='Pending').count(),
        'completed_bookings': Booking.objects.filter(status='Completed').count(),
    }
    return render(request, 'owner_dashboard/dashboard.html', context)

#Admin Dashbord
def admin_dashboard(request):
    context = {
        'users_count': User.objects.count(),
        'pending_bookings': Booking.objects.filter(status='Pending').count(),
        'completed_bookings': Booking.objects.filter(status='Completed').count(),
    }
    return render(request, 'admin_dashboard/dashboard.html', context)

def manage_users(request):
    users = User.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'admin_dashboard/manage_users.html', context)

@csrf_exempt
def get_users_api(request):
    users = User.objects.all()
    user_data = []
    for user in users:
        user_data.append({
            'id': user.id,
            'full_name': user.get_full_name(),
            'email': user.email,
            'phone': user.phone,
        })
    return JsonResponse({'users': user_data})
    

def create_user(request):
    if request.method == 'POST':
        # Validate the form data using the custom manager's validator
        errors = User.objects.register_validator(request.POST)
        
        # If there are validation errors, return the form with error messages
        if errors:
            # Pass POST data back to the form to retain user input after validation failure
            return render(request, 'admin_dashboard/create_user.html', {'errors': errors, 'postData': request.POST})
           
        # If no errors, create the new user
        user = User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            phone=request.POST.get('phone', ''),
            password=make_password(request.POST['password']),
        )
        
        messages.success(request, "User created successfully")
        return redirect('landing:dashbord') 
    
    # If the request method is GET, render the form (no errors)
    return render(request, 'admin_dashboard/create_user.html')

def update_user_view(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return HttpResponse("User Not Found", status=404)
    return render(request, 'admin_dashboard/update_user.html', {'user_obj': user})    
        

@csrf_exempt
def update_user_api(request, user_id):
    if request.method == "POST":
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User not found'})

        data = request.POST
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.email = data['email']
        user.phone = data.get('phone', '')
        user.save()

        return JsonResponse({
            'success': True,
            'user_id': user.id,
            'full_name': user.get_full_name(),
            'email': user.email,
            'redirect_url': reverse('landing:dashbord')
        })
    
    return JsonResponse({
       'success': True,
       'message': "User updated successfully",
       'redirect_url': reverse('landing:dashbord')
    })
  
@csrf_exempt
def delete_user(request, user_id):
    if request.method == "POST":
        user = User.objects.get(id=user_id)
        user.delete()
        return JsonResponse({'success': True, 'user_id': user_id})
   
def manage_users(request):
    users = User.objects.all().order_by('-id')
    
    data = [
        {'name': f'User {i}', 'description': f'Description {i}'} for i in range(1, 21)
    ]
    paginator = Paginator(data, 5)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'users': users,
        'page_obj': page_obj
    }

    return render(request, 'admin_dashboard/manage_users.html',context)

def manage_users(request):
    users = User.objects.all().order_by('-id')
    
    data = [
        {'name': f'User {i}', 'description': f'Description {i}'} for i in range(1, 21)
    ]
    paginator = Paginator(data, 5)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'users': users,
        'page_obj': page_obj
    }

    return render(request, 'admin_dashboard/manage_users.html', context)
from django.shortcuts import render, HttpResponse


def workshop_list(request):
    workshops = Workshop.objects.all()
    return render(request, 'admin_dashboard/manage_workshops.html', {'workshops': workshops})
@csrf_exempt    
def workshop_create(request):
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
                image=image
            )
            return redirect('landing:workshop_list')
        else:
            return HttpResponse("Address is required", status=400)
  
    addresses = Address.objects.all()
    return render(request, 'admin_dashboard/create.html', {'addresses': addresses})

      




def edith(request):
    workshop = Workshop.objects.first()  
    addresses = Address.objects.all()
    return render(request, 'admin_dashboard/update_workshop.html', {
        'workshop': workshop,
        'addresses': addresses,
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
        image = request.FILES.get('image')

       
        workshop.name = name
        workshop.phone = phone
        workshop.address_id = address_id
        workshop.image = image

        workshop.save()

        return JsonResponse({'status': 'updated'})


@csrf_exempt
def delete(request, id):
    if request.method == 'POST':
        try:
            workshop = Workshop.objects.get(id=id)
        except Workshop.DoesNotExist:
            return JsonResponse({'error': 'Workshop not found'}, status=404)

        workshop.delete()
        return JsonResponse({'status': 'deleted'})
def service_list(request):
    services = Service.objects.all()
    return render(request, 'admin_dashboard/service_list.html', {'services': services}) 

@csrf_exempt
def service_create(request):
    # إذا كان الطلب GET، يرجع صفحة HTML (النموذج)
    if request.method == 'GET':
        # يمكنك هنا إعادة نفس الصفحة أو نموذج جديد
        workshops = Workshop.objects.all()
        return render(request, 'admin_dashboard/create_service.html', {'workshops': workshops})

    # إذا كان الطلب POST، إضافة الخدمة الجديدة
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        description = request.POST['description']
        duration = request.POST['duration']
        workshop_id = request.POST['workshop_id']

        workshop = Workshop.objects.get(id=workshop_id)

        service = Service.objects.create(
            name=name,
            price=price,
            description=description,
            duration=duration,
            workshop=workshop
        )

        return JsonResponse({
            'id': service.id,
            'name': service.name,
            'price': service.price,
            'description': service.description,
            'duration': service.duration
        })
        
@csrf_exempt
def service_delete(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    
    if request.method == 'POST':
        service.delete()
        return JsonResponse({'status': 'deleted'})
def service_update(request, service_id):
    service = get_object_or_404(Service, id=service_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        duration = request.POST.get('duration')

        service.name = name
        service.price = price
        service.description = description
        service.duration = duration
        service.save()

        return JsonResponse({
            'id': service.id,
            'name': service.name,
            'price': service.price,
            'description': service.description,
            'duration': service.duration
        })        