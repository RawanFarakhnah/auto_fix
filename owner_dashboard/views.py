from django.db.models import Count, Q
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import get_user_model
from django.urls import reverse
from workshops.models import Workshop, Service
from reviews.models import Review
from bookings.models import Booking, Notification
from locations.models import Address
from reviews.models import Review
from cars.models import Car
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from workshops.models import Address,Service
from django.db.models import Count, Avg, Sum
from datetime import date, timedelta

# get user model
User = get_user_model()

#owner Dashbord
def dashboard(request):
    if not request.user.is_workshop_owner:
        return redirect('landing:main')
    if not Workshop.objects.filter(owner = request.user):
        return redirect('owner_dashboard:workshop')
    workshop = Workshop.objects.filter(owner=request.user).first()
    
    if not workshop:
        return render(request, 'owner_dashboard/dashboard.html', {'workshops': []})

    today = date.today()
    
    # Bookings stats
    bookings = Booking.objects.filter(workshop=workshop)
    total_bookings = bookings.count()
    today_bookings = bookings.filter(appointment_date__date=today).count()
    pending_bookings = bookings.filter(status='pending').count()
    
    # Revenue calculation
    monthly_revenue = bookings.filter(
        status='completed',
        appointment_date__month=today.month,
        appointment_date__year=today.year
    ).aggregate(total=Sum('service__price'))['total'] or 0
    
    # Review stats
    reviews = Review.objects.filter(service__workshop=workshop)
    average_rating = reviews.aggregate(avg=Avg('rating'))['avg'] or 0
    
    # Recent data
    recent_bookings = bookings.select_related(
        'user', 'service'  # Removed 'vehicle' as it doesn't exist in your model
    ).order_by('-appointment_date')[:5]
    
    # Get services with booking counts
    popular_services = Service.objects.filter(
        workshop=workshop
    ).annotate(
        booking_count=Count('booking'),  # Using default related_name
        avg_rating=Avg('review__rating')
    ).order_by('-booking_count')[:4]
    
    recent_reviews = reviews.select_related(
        'user', 'service'
    ).order_by('-created_at')[:4]

    context = {
        'workshops': [workshop],
        'stats': {
            'total_bookings': total_bookings,
            'today_bookings': today_bookings,
            'pending_bookings': pending_bookings,
            'monthly_revenue': monthly_revenue,
            'average_rating': round(average_rating, 1),
        },
        'recent_bookings': recent_bookings,
        'popular_services': popular_services,
        'recent_reviews': recent_reviews,
    }
    return render(request, 'owner_dashboard/dashboard.html', context)

def workshop_management(request):
    # Workshop management view logic
    if not request.user.is_workshop_owner:
        return redirect('landing:main')
    if request.method == "POST":
        errors = Workshop.objects.validation(request.POST)
        if len(errors)>0:
           for key,value in errors.items():
               messages.error(request,value) 
        else:
            name = request.POST['name']
            phone = request.POST['phone']
            description = request.POST['description']
            image = request.FILES['workshop_image']
            street = request.POST['street']
            city = request.POST['city']
            region = request.POST['region']
            country = request.POST['country']
            postal_code = request.POST['postal_code']
            the_address = Address.objects.create(
                street = street,
                city =city,
                region = region,
                country = country,
                postal_code = postal_code
            )
            Workshop.objects.create(
                name = name ,
                phone = phone ,
                description = description ,
                image = image ,
                owner = request.user,
                address = the_address
            )
    try:
        workshop = Workshop.objects.get(owner=request.user)
        total_services = workshop.services.count()
        total_bookings = workshop.booking_set.count()
        
        # Calculate average rating
        reviews = workshop.review_set.all()
        avg_rating = None

        context = {
            'workshop': workshop,
            'total_services': total_services,
            'total_bookings': total_bookings,
            'avg_rating': round(avg_rating, 1) if avg_rating else None
        }
    except Workshop.DoesNotExist:
        context = {'workshop': None}
        
    return render(request, 'owner_dashboard/workshop.html', context)
        


@csrf_exempt
def delete_workshop(request):
      # Delete workshop view logic
    if not request.user.is_workshop_owner:
        return redirect('landing:main')
    if request.method == 'POST':
        workshop_id = request.POST.get('id')  
        try:
            workshop = Workshop.objects.get(id=workshop_id)
            workshop.delete()
            return JsonResponse({'status': 'deleted'})
        except Workshop.DoesNotExist:
            return JsonResponse({'error': 'Workshop not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def change_image(request):
    if not request.user.is_workshop_owner:
        return redirect('landing:main')
    if request.method == 'POST':
        image = request.FILES['Workshop_image']
        workshop = Workshop.objects.get(owner = request.user)
        workshop.image = image
        workshop.save()
        return redirect('owner_dashboard:workshop')
    
def edit_workshop(request):
    # Edit workshop view logic
    if not request.user.is_workshop_owner:
        return redirect('landing:main')
    if request.method == 'POST':
        workshop = Workshop.objects.get(owner = request.user)
        workshop.name = request.POST['name']
        workshop.phone = request.POST['phone']
        workshop.description =  request.POST['description']
        workshop.save()
        address = workshop.address
        address.street = request.POST['street']
        address.city = request.POST['city']
        address.region = request.POST['region']
        address.country = request.POST['country']
        address.postal_code = request.POST['postal_code']
        address.save()
        return redirect('owner_dashboard:workshop')

def register_workshop(request):
    # register workshop view logic
    pass

def services_management(request):
    try:
        workshop = request.user.workshop
        services = Service.objects.filter(workshop=workshop)
        
        context = {
            'services': services,
        }
    except Workshop.DoesNotExist:
        messages.warning(request, "You need to register a workshop first")
        return redirect('owner_dashboard:workshop')
    
    return render(request, 'owner_dashboard/services.html', context)

def add_service(request):
    # Add service view logic
    if not request.user.is_workshop_owner:
        return redirect('landing:main')
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
    

def edit_service(request, service_id):
    # Edit service view logic
    if not request.user.is_workshop_owner:
        return redirect('landing:main')
    if request.method == 'POST':
        service = Service.objects.get(id = service_id)
        service.name= request.POST['name']
        service.price= request.POST['price']
        service.description= request.POST['description']
        service.duration= request.POST['duration']
        service.save()
        return redirect('owner_dashboard:services')
    

def delete_service(request, service_id):
    # Delete service view logic
    if not request.user.is_workshop_owner:
        return redirect('landing:main')
    service = Service.objects.get(id = service_id)
    service.delete()
    return redirect('owner_dashboard:services')


def bookings_management(request):
    # Bookings management view logic
    pass

def update_booking_status(request, booking_id):
    # Update booking status view logic
    pass

def reviews_management(request):
    try:
        workshop = request.user.workshop
    except AttributeError:
        return redirect('owner_dashboard:workshop')
    
    reviews = Review.objects.filter(workshop=workshop).order_by('-created_at')
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    total_reviews = reviews.count()
    
    context = {
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1) if avg_rating else None,
        'total_reviews': total_reviews,
    }
    
    return render(request, 'owner_dashboard/reviews.html', context)
   

def reply_review(request, review_id):
    # Reply to review view logic
    pass

##-----------------------------------------------------------------------###

def owner_dashboard(request):
    if not request.user.is_authenticated or not request.user.is_workshop_owner:
        return redirect('landing:main')
    
    workshop = Workshop.objects.filter(owner=request.user).first()
    recent_bookings = Booking.objects.filter(workshop=workshop).order_by('-appointment_date')[:5] if workshop else []
    
    context = {
        'workshops': [workshop] if workshop else [],
        'recent_bookings': recent_bookings,
    }
    return render(request, 'owner_dashboard/dashboard.html', context)

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

def edit_workshop1(request, id):
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



