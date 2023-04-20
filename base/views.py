from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request, 'home.html', context={})

def contact(request):
    return render(request, 'contact.html', context={})

def about(request):
    return render(request, 'about.html', context={})