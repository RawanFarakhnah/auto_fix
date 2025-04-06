from django.shortcuts import render

# Create your views here.
def main(request):
    return render(request, 'landing\main.html')

def contact(request):
    return render(request, 'landing\contact.html')

def dashbord(request):
    return render(request, 'landing\dashbord.html')