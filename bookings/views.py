from django.shortcuts import render, HttpResponse

# Create your views here.
def bookings_list(request):
    return HttpResponse("workshops list")