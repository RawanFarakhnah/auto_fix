
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout

def user_register(request):
    if request.user.is_authenticated:
        return redirect('landing:dashbord')
    
    if request.method == 'POST':
        errors = User.objects.register_validator(request.POST)

        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('landing:register')

        user = User.objects.create(
            first_name_en=request.POST['first_name_en'],
            last_name_en=request.POST['last_name_en'],
            first_name_ar=request.POST['first_name_ar'],
            last_name_ar=request.POST['last_name_ar'],
            email=request.POST['email'],
            password=make_password(request.POST['password']),
        )

        login(request, user)  # automatically saves user in session
        messages.success(request, "Registered Successfully")
        return redirect('landing:dashbord')

    return render(request, 'accounts/register.html')

def user_login(request):
    if request.user.is_authenticated:
        return redirect('landing:dashbord')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(email=email, password=password)

        if user is None:
            messages.error(request, "Email or Password is incorrect", extra_tags="login")
            return redirect('landing:login')

        login(request, user)
        messages.success(request, "Logged in Successfully")
        return redirect('landing:dashbord')

    return render(request, 'accounts/login.html')

def user_profile(request):
    if not request.user.is_authenticated:
        return redirect('landing:home')
    
    #user = User.objects.get(id=request.session['user_id']) 
    return render(request, 'accounts/profile.html', {'user': request.user})

def user_logout(request):
   if not request.user.is_authenticated:
        return redirect('landing:home')

   logout(request)
   return redirect('landing:home')