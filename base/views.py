from django.shortcuts import render, redirect
from .forms import ContactForm


def home(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            return redirect("home")
        else:
            form = ContactForm(request.POST)
            return render(request, 'home.html', {'form':form})
    form = ContactForm()
    return render(request, 'home.html', context={})