from django.db.models import Count, Q
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
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
        
        # Show a success message
        messages.success(request, "User created successfully")
        
        # Redirect to the dashboard or a different page
        return redirect('landing:dashbord')  # Make sure this URL is correct in your urls.py
    
    # If the request method is GET, render the form (no errors)
    return render(request, 'admin_dashboard/create_user.html')


    

@csrf_exempt
def update_user_api(request, user_id):
    if request.method == "POST":
        user = User.objects.get(id=user_id)
        data = request.POST
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.email = data['email']
        user.phone = data.get('phone', '')
        user.save()
        return JsonResponse({'success': True, 'user_id': user.id, 'full_name': user.get_full_name(), 'email': user.email})
@csrf_exempt
def delete_user(request, user_id):
    if request.method == "POST":
        user = User.objects.get(id=user_id)
        user.delete()
        return JsonResponse({'success': True, 'user_id': user_id})