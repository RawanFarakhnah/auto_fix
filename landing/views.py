from django.shortcuts import render

# Create your views here.
def root(request):
    return render(request, 'landing.html')
def dashboard(request):
    return render(request,'dashboard.html')
def user(request):
    return render(request,'user/user.html')
def add_user(request):
    return render(request,'user/add_user.html')
def update_user(request,user_id):
    return render(request,'user/update_user.html')
def update_booking(request):
    return render(request,'booking/add_booking.html')
def add_book(request):
    return render(request,'booking/booking.html')
def add_workshop(request):
    return render(request,'workshop/add_workshop.html')
def list_workshop(request):
    return render(request,'workshop/workshop.html')
def add_review(request):
    return render(request,'review/add_review.html')
def list_review(request):
    return render(request,'review/list_review.html')
def admin_review(request):
    return render(request,'review/admin_review.html')


 
