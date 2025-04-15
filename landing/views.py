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
        return redirect('landing:dashboard')

    context = {
        "reviews" : Review.objects.all()[:3]
    }
    return render(request, 'landing\main.html')

def contact(request):
    return render(request, 'landing\contact.html')

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

# def reviews_list(request):
#     reviews = Review.objects.select_related('user', 'workshop', 'service').all()
#     return render(request, 'landing/main.html', {'reviews': reviews})