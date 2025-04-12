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
        workshop = Workshop.objects.filter(owner = request.user.id)
        context = {
            'workshops':workshop
        }
        return render(request, 'owner_dashboard/dashboard.html',context)

    return redirect('landing:main')


def manage_workshops(request):
    if request.user.is_authenticated and request.user.is_workshop_owner:
        user_id = request.user.id
        try:
            workshops = Workshop.objects.filter(owner = user_id)
            return render(request, 'owner_dashboard/manage_workshops.html', {'workshops': workshops})
        except:
            return redirect('owner_dashboard:dashboard')
    return redirect('landing:main')
  
def create_workshop(request):
    if request.user.is_authenticated and request.user.is_workshop_owner:
        addresses = Address.objects.all()
        if request.method == 'POST':
            errors = Workshop.objects.validation(request.POST)
            if len(errors) > 0 :
                for key,value in errors.items():
                    messages.error(request,value)
                return render(request,'owner_dashboard/create_workshop.html',{'addresses': addresses})
            else:
                name = request.POST.get('name')
                phone = request.POST.get('phone')
                address_id = request.POST.get('address_id')
                image = request.FILES.get('image')
                description = request.POST['description']
                if address_id:  
                    Workshop.objects.create(
                        name=name,
                        phone=phone,
                        address_id=address_id,
                        image=image,
                        owner = request.user,
                        description= description
                        )
                    
                    return redirect('owner_dashboard:manage_workshops')
                else:
                    return HttpResponse("Address is required", status=400)
        
       
        return render(request, 'owner_dashboard/create_workshop.html', {'addresses': addresses})
    return redirect('landing:main')

def edit_workshop(request, id):
    if request.user.is_authenticated and request.user.is_workshop_owner:
        workshop = Workshop.objects.get(id=id)
        addresses = Address.objects.all()
        return render(request, 'owner_dashboard/update_workshop.html', {
            'workshop': workshop,
            'addresses': addresses,
        })
    return redirect('landing:main')

@csrf_exempt
def workshop_update(request, id):
    if request.user.is_authenticated and request.user.is_workshop_owner:
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
    return redirect('landing:main')

@csrf_exempt
def delete_workshop(request, id):
    if request.user.is_authenticated and request.user.is_workshop_owner:
        if request.method == 'POST':
            try:
                workshop = Workshop.objects.get(id=id)
                workshop.delete() 
                return JsonResponse({'status': 'deleted'})
            except Workshop.DoesNotExist:
                return JsonResponse({'error': 'Workshop not found'}, status=404)
        return JsonResponse({'error': 'Invalid request'}, status=400)
    return redirect('landing:main')

def services(request):
    if request.user.is_authenticated and request.user.is_workshop_owner:
        try:
            workshop = Workshop.objects.get(owner = request.user.id)
            services = Service.objects.filter(workshop = workshop)
            context = {
                'services': services
            }
            return render(request, 'owner_dashboard/mange_services.html', context)
        except:
            return redirect('owner_dashboard:dashboard') 
    return redirect('landing:main')

@csrf_exempt
def service_create(request):
    if request.user.is_authenticated and request.user.is_workshop_owner:
        workshops = Workshop.objects.filter(owner = request.user.id)
        if request.method == 'POST':
            name = request.POST['name']
            price = request.POST['price']
            description = request.POST['description']
            duration = request.POST['duration']
            workshop = Workshop.objects.get(owner = request.user.id)

            service = Service.objects.create(
                name=name,
                price=price,
                description=description,
                duration=duration,
                workshop=workshop
            )

            return redirect('owner_dashboard:services')
        return render(request, 'owner_dashboard/create_service.html', {'workshops': workshops})
    return redirect('landing:main')


@csrf_exempt
def delete_service(request, service_id):
    if request.user.is_authenticated and request.user.is_workshop_owner:
        service = Service.objects.get(id = service_id)
        service.delete()
        return redirect('owner_dashboard:services')
    return redirect('landing:main')


def bookings(request):
    if request.user.is_authenticated and request.user.is_workshop_owner:
        try:
            workshop = Workshop.objects.get(owner = request.user.id)
            bookings = Booking.objects.get(workshop = workshop)
            context= {
                'bookings':bookings,
                'workshop':workshop
            }
            return render(request,'owner_dashboard/bookings.html',context)
        except:
            context ={
                'workshop':False
            }
            return render(request,'owner_dashboard/bookings.html',context)
    return redirect('landing:main')

def update_booking(request):
    if request.method == "POST" and request.user.is_authenticated:
        booking_id = request.POST.get('id')
        new_status = request.POST.get('status')
        
        booking = Booking.objects.get(id=booking_id)
        booking.status = new_status
        booking.save()
        Notification.objects.create(
            user=booking.user,
            booking=booking,
            message=f"booking have been updated to {new_status}"
        )
        return JsonResponse({"message": "Booking updated successfully", "status": new_status})

    return redirect('landing:main')



