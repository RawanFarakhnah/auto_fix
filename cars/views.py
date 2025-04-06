from django.shortcuts import render, HttpResponse

# Create your views here.
def cars_list(request):
    return HttpResponse("cars list")