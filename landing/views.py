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
 
