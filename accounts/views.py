
import re
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from locations.models import Address
from django.conf import settings

def user_register(request):
    if request.user.is_authenticated:
        return redirect('landing:dashboard')
    
    if request.method == 'POST':
        errors = User.objects.register_validator(request.POST)

        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('landing:register')

        user = User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            phone=request.POST.get('phone', ''),
            password=make_password(request.POST['password']),
        )

        login(request, user)  # automatically saves user in session
        messages.success(request, "Registered Successfully")
        return redirect('landing:dashboard')

    return render(request, 'accounts/register.html')

def user_login(request):
    if request.user.is_authenticated:
        return redirect('landing:dashboard')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(email=email, password=password)

        if user is None:
            messages.error(request, "Email or Password is incorrect", extra_tags="login")
            return redirect('landing:login')

        login(request, user)
        messages.success(request, "Logged in Successfully")
        return redirect('landing:dashboard')

    return render(request, 'accounts/login.html')

def user_logout(request):
   if not request.user.is_authenticated:
        return redirect('landing:main')

   logout(request)
   return redirect('landing:main')

#Profile Region
def profile(request):
    if not request.user.is_authenticated:
        return redirect('landing:main')
    
    context = {
        'user': request.user,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
    }
    return render(request, 'accounts/profile.html', context)

def profile_update(request):
    if not request.user.is_authenticated:
        return redirect('landing:main')
    
    if request.method == "POST":
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        phone = request.POST.get('phone', '')
        
        # Validate phone number format
        if phone and not re.match(r'^\d{3}-\d{3}-\d{4}$', phone):
            messages.error(request, "Please enter phone in format: 800-555-1234")
        else:
            user.phone = phone
            user.save()
            messages.success(request, "Profile updated successfully")
        
        return redirect('accounts:profile')
    
    return redirect('accounts:profile')

def profile(request):
    if not request.user.is_authenticated:
        return redirect('landing:main')
    
    context = {
        'user': request.user,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
    }
    return render(request, 'accounts/profile.html', context)

def update_address(request):
    if request.method != 'POST':
        return redirect('accounts:profile#address')
    
    user = request.user
    street = request.POST.get('street', '').strip()
    city = request.POST.get('city', '').strip()
    region = request.POST.get('region', '').strip()
    country = request.POST.get('country', '').strip()
    postal_code = request.POST.get('postal_code', '').strip()
    
    # Make coordinates optional with default None
    latitude = request.POST.get('latitude', '').strip() or None
    longitude = request.POST.get('longitude', '').strip() or None
    
    # Validate required fields
    if not all([street, city, country]):
        messages.error(request, "Street, City and Country are required fields")
        return redirect('accounts:profile#address')
    
    try:
        # Convert coordinates if provided
        if latitude is not None:
            latitude = float(latitude)
            if not (-90 <= latitude <= 90):
                raise ValueError("Latitude must be between -90 and 90")
        
        if longitude is not None:
            longitude = float(longitude)
            if not (-180 <= longitude <= 180):
                raise ValueError("Longitude must be between -180 and 180")
            
        # Create or update address
        if user.address:
            address = user.address
            address.street = street
            address.city = city
            address.region = region
            address.country = country
            address.postal_code = postal_code
            if latitude: address.latitude = latitude
            if longitude: address.longitude = longitude
        else:
            address = Address.objects.create(
                street=street,
                city=city,
                region=region,
                country=country,
                postal_code=postal_code,
                latitude=latitude,
                longitude=longitude
            )
            user.address = address
        
        address.save()
        user.save()
        messages.success(request, "Address updated successfully")
        
    except ValueError as e:
        messages.error(request, str(e))
    except Exception as e:
        messages.error(request, f"Error saving address: {str(e)}")
    
    return redirect('accounts:profile#address')


def change_password(request):
    pass

def delete_account(request):
    pass