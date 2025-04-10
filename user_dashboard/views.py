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

#user Dashbord
def user_dashboard(request):
    if request.user.is_authenticated and not ( request.user.is_workshop_owner or request.user.is_superuser ):        
        return render(request, 'user_dashboard/dashboard.html')

    return redirect('landing:main')