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
        return render(request, 'owner_dashboard/dashboard.html')

    return redirect('landing:main')


def manage_workshops(request):
    workshops = Workshop.objects.all()
    return render(request, 'owner_dashboard/manage_workshops.html', {'workshops': workshops})
  
def create_workshop(request):
    if request.method == 'POST':
        #TODO: Back Validation 
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
            
            return redirect('owner_dashboard:manage_workshops')
        else:
            return HttpResponse("Address is required", status=400)
  
    addresses = Address.objects.all()
    return render(request, 'owner_dashboard/create_workshop.html', {'addresses': addresses})


def edit_workshop(request, id):
    workshop = Workshop.objects.get(id=id)
    addresses = Address.objects.all()
    return render(request, 'owner_dashboard/update_workshop.html', {
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
        address_id = request.POST['address_id']
        image = request.FILES.get('image')

        if name:
            workshop.name = name
        if phone:
            workshop.phone = phone
        if address_id:
            workshop.address_id = address_id
        if image:
            workshop.image = image

        workshop.save()
        return JsonResponse({'status': 'updated', 'name': name, 'phone': phone})

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def delete_workshop(request, id):
    if request.method == 'POST':
        try:
            workshop = Workshop.objects.get(id=id)
            workshop.delete() 
            return JsonResponse({'status': 'deleted'})
        except Workshop.DoesNotExist:
            return JsonResponse({'error': 'Workshop not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)
