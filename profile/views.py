from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import NewUserForm


def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("profile:dashboard")
            else:
                return render(request, 'profile/login.html', {"form":form})
    else:
        form = AuthenticationForm()
    return render(request, 'profile/login.html', {"form": form})

def register_user(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("profile:dashboard")
        else:
            form = NewUserForm(request.POST)
            return render(request, 'profile/register.html', {'form':form})
    form = NewUserForm()
    return render(request, 'profile/register.html', {'form':form})

def logout_user(request):
    logout(request)
    return redirect("home")

def dashboard(request):
    return render(request, 'profile/dashboard.html', context={})
