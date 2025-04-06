from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'landing\home.html')

def contact(request):
    return render(request, 'landing\contact.html')

def dashbord(request):
    return render(request, 'landing\dashbord.html')