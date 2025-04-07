from django.db.models import Count, Q
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from workshops.models import Workshop, Service
from reviews.models import Review
from bookings.models import Booking
from locations.models import Address
from cars.models import Car

# Create your views here.
User = get_user_model()

def main(request):
    return render(request, 'landing\main.html')

def contact(request):
    return render(request, 'landing\contact.html')

def dashbord(request):
    if User.is_superuser:
        return redirect('landing:admin_dashboard')
    return redirect('landing:admin_dashboard')

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