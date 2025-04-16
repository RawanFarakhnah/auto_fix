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
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
User = get_user_model()

def main(request):
    if request.user.is_authenticated:
        return redirect('landing:dashboard')

    context = {
        "reviews" : Review.objects.all()[:3]      
    }
    return render(request, 'landing\main.html',context)



def dashboard(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_dashboard:dashboard')
        elif request.user.is_workshop_owner:
            return redirect('owner_dashboard:dashboard')
        else:
            return redirect('user_dashboard:dashboard')
    else:
        return redirect('landing:main')       




def send_contact_message(request):
    print("🚀 View reached!")

   

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        print("Received Data:", name, email, message)  

        subject = f"New message from {name} via AutoFix"
        full_message = f"From: {name} <{email}>\n\nMessage:\n{message}"

        try:
            send_mail(
                subject,
                full_message,
                'yasmeenabassam85@gmail.com',
                ['yasmeenabassam85@gmail.com'],
                fail_silently=False,
            )
            print("Email sent successfully!")
        except Exception as e:
            print("Error while sending email:", e)

        return redirect('landing:main')

    return redirect('landing:main')
