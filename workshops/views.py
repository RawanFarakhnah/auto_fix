from django.shortcuts import render, HttpResponse

# Create your views here.
def workshops_list(request):
    return HttpResponse("workshops list")