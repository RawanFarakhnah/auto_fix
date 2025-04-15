from django.db.models import Count, Q
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from workshops.models import Workshop, Service
from reviews.models import Review
from bookings.models import Booking, Notification
from locations.models import Address
from reviews.models import Review
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import JsonResponse
from workshops.models import Address,Service
from django.db.models import Count, Avg, Sum
from datetime import date
from django.shortcuts import get_object_or_404


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
    if not request.user.is_workshop_owner:
        return JsonResponse({"status": "error", "message": "Unauthorized"}, status=403)

    if request.method == "POST":
        errors = {}
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        description = request.POST.get('description', '').strip()
        street = request.POST.get('street', '').strip()
        city = request.POST.get('city', '').strip()
        region = request.POST.get('region', '').strip()
        country = request.POST.get('country', '').strip()
        postal_code = request.POST.get('postal_code', '').strip()
        image = request.FILES.get('workshop_image')

        if not name:
            errors['name'] = "Workshop name is required!"
        if not phone or not phone.isdigit():
            errors['phone'] = "Phone number must contain only digits!"
        if not description or len(description) < 10:
            errors['description'] = "Description must be at least 10 characters long!"
        if not street:
            errors['street'] = "Street address is required!"
        if not city:
            errors['city'] = "City is required!"
        if not region:
            errors['region'] = "Region/State is required!"
        if not country:
            errors['country'] = "Country is required!"
        if not postal_code or not postal_code.isdigit():
            errors['postal_code'] = "Postal code must contain only digits!"
        if not image:
            errors['workshop_image'] = "Workshop image is required!"

        if errors:
            return JsonResponse({"status": "error", "messages": errors})  

        the_address = Address.objects.create(
            street=street,
            city=city,
            region=region,
            country=country,
            postal_code=postal_code
        )
        Workshop.objects.create(
            name=name,
            phone=phone,
            description=description,
            image=image,
            owner=request.user,
            address=the_address
        )

        return JsonResponse({"status": "success", "message": "Workshop registered successfully!"})  # ✅ إرجاع رسالة نجاح

    try:
        workshop = Workshop.objects.get(owner=request.user)
        context = {
            'workshop': workshop,
            'total_services': workshop.services.count(),
            'total_bookings': workshop.booking_set.count(),
            'avg_rating': round(workshop.review_set.aggregate(Avg('rating'))['rating__avg'], 1) if workshop.review_set.exists() else None
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
    if not request.user.is_workshop_owner:
        return JsonResponse({"status": "error", "message": "Unauthorized"}, status=403)

    if request.method == 'POST':
        errors = {}  

        try:
            workshop = get_object_or_404(Workshop, owner=request.user)
        except Workshop.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Workshop not found"}, status=404)

    
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        description = request.POST.get('description', '').strip()


        if not name:
            errors['name'] = "Workshop name is required!"
        elif not name.replace(" ", "").isalpha(): 
            errors['name'] = "Workshop name must contain only letters!"
        
        if not phone or not phone.isdigit():
            errors['phone'] = "Phone number must contain only digits!"
        
        if not description or len(description) < 10:
            errors['description'] = "Description must be at least 10 characters long!"

        if errors:
            return JsonResponse({"status": "error", "messages": errors})  

      
        workshop.name = name
        workshop.phone = phone
        workshop.description = description
        workshop.save()

        return JsonResponse({"status": "success", "message": "Workshop updated successfully!"})  



def services_management(request):
    if not request.user.is_workshop_owner:
        return redirect('landing:main')
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
    if not request.user.is_workshop_owner:
        return JsonResponse({"status": "error", "message": "Unauthorized"}, status=403)

    if request.method == 'POST' :
        errors= {}    
        name = request.POST.get('name', '').strip()
        price = request.POST.get('price')
        duration = request.POST.get('duration')

        if not name:
            errors['name'] = "Service name is required!"
        if not price or float(price) <= 0:
            errors['price'] = "Price must be greater than zero!"
        if not duration or int(duration) <= 0:
            errors['duration'] = "Duration must be a positive number!"
        
        workshop = get_object_or_404(Workshop, owner=request.user)
        Service.objects.create(
            name=request.POST['name'],
            price=request.POST['price'],
            description=request.POST['description'],
            duration=request.POST['duration'],
            workshop=workshop
        )

        return JsonResponse({"status": "success", "message": "Service added successfully!"})  
    


def edit_service(request, service_id):
    if not request.user.is_workshop_owner:
        return JsonResponse({"status": "error", "message": "Unauthorized"}, status=403)

    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST' :
        errors= {}    
        name = request.POST.get('name', '').strip()
        price = request.POST.get('price')
        duration = request.POST.get('duration')

        if not name:
            errors['name'] = "Service name is required!"
        if not price or float(price) <= 0:
            errors['price'] = "Price must be greater than zero!"
        if not duration or int(duration) <= 0:
            errors['duration'] = "Duration must be a positive number!"

        if errors:
            return JsonResponse({"status": "error", "messages": errors})  

        service.name = request.POST.get('name', '')
        service.price = request.POST['price']
        service.description = request.POST['description']
        service.duration = request.POST['duration']
        service.save()

        return JsonResponse({"status": "success", "message": "Service updated successfully!"})  
    

def delete_service(request, service_id):
    # Delete service view logic
    if not request.user.is_workshop_owner:
        return redirect('landing:main')
    service = Service.objects.get(id = service_id)
    service.delete()
    return redirect('owner_dashboard:services')


def bookings_management(request):
    # Bookings management view logic
    if not request.user.is_workshop_owner:
        return redirect('landing:main')
    workshop = Workshop.objects.filter(owner = request.user).first()
    bookings = Booking.objects.filter(workshop=workshop)
    status = request.GET.get('status', '')
    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')

    if status:
        bookings = bookings.filter(status=status)
    if from_date:
        bookings = bookings.filter(appointment_date__gte=from_date)
    if to_date:
        bookings = bookings.filter(appointment_date__lte=to_date)

    
    context = {
        'bookings': bookings,
    }

    return render(request,'owner_dashboard/bookings.html',context)

def confirm_booking(request,booking_id):
    if not request.user.is_workshop_owner:
        return redirect('landing:main')
    booking = Booking.objects.get(id = booking_id)
    booking.status = 'confirmed'
    booking.save()
    notification = Notification.objects.create(
        user = booking.user,
        message = f"The {booking.service.name} have been changed to {booking.status}",
        booking = booking
    )
    return redirect('owner_dashboard:bookings')

def cancel_booking(request,booking_id):
    if not request.user.is_workshop_owner:
        return redirect('landing:main')
    booking = Booking.objects.get(id = booking_id)
    booking.status = 'canceled'
    booking.save()
    notification = Notification.objects.create(
        user = booking.user,
        message = f"The {booking.service.name} have been changed to {booking.status}",
        booking = booking
    )
    return redirect('owner_dashboard:bookings')

def complete_booking(request,booking_id):
    if not request.user.is_workshop_owner:
        return redirect('landing:main')
    booking = Booking.objects.get(id = booking_id)
    booking.status = 'completed'
    booking.save()
    notification = Notification.objects.create(
        user = booking.user,
        message = f"The {booking.service.name} have been changed to {booking.status}",
        booking = booking
    )
    return redirect('owner_dashboard:bookings')


def update_booking_status(request, booking_id):
    # Update booking status view logic
    if not request.user.is_workshop_owner:
        return JsonResponse({"status": "error", "message": "Unauthorized"}, status=403)
    booking = Booking.objects.get(id = booking_id)
    new_status = request.GET.value
    if new_status in ['pending', 'confirmed', 'completed', 'canceled']:
        booking.status = new_status
        booking.save()
        return JsonResponse({'status': 'success', 'message': f'Updated to {new_status} successfuly!'})
    
    return JsonResponse({'status': 'error', 'message': 'Error'}, status=400)


def reviews_management(request):
    if not request.user.is_workshop_owner:
        return redirect('landing:main')
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
    if not request.user.is_workshop_owner:
        return JsonResponse({"status": "error", "message": "Unauthorized"}, status=403)
    
    if request.method == 'POST':
        review_id = request.POST.get('review_id')
        response_text = request.POST.get('response_text')

        review = get_object_or_404(Review, id=review_id)
        
        if not response_text.strip():
            return JsonResponse({'status': 'error', 'message': 'Please type valid response!'}, status=400)

        review.response = response_text
        review.save()
        
        return JsonResponse({'status': 'success', 'message': 'Your response sent succesfully!'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid response , Try again!'}, status=400)
  


##-----------------------------------------------------------------------###



