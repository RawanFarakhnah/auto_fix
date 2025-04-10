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

# get user model
User = get_user_model()

#owner Dashbord
def owner_dashboard(request):
    if request.user.is_authenticated and request.user.is_workshop_owner:
        context = {
        
        'users_count': User.objects.count(),
        'pending_bookings': Booking.objects.filter(status='Pending').count(),
        'completed_bookings': Booking.objects.filter(status='Completed').count(),
        }
        return render(request, 'owner_dashboard/dashboard.html', context)

    return redirect('landing:main')