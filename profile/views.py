from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import NewUserForm

from django.contrib.staticfiles.storage import staticfiles_storage
import pickle
import pandas as pd

#model_url = staticfiles_storage.path('data/model.pkl')
model = pickle.load(open("static/data/model.pkl","rb"))
#transformer_url = staticfiles_storage.url('data/transformer.pkl')
transformer = pickle.load(open("static/data/transformer.pkl","rb"))


def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("profile:dashboard_home")
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

def dashboard_home(request):
    return render(request, 'dashboard/summary.html', context={})

def dashboard_bodystats(request):
    body_stats = {
        "Age": [22],
        "Weight": [173.25],
        "Height": [72.25],
        "Neck": [38.50],
        "Chest": [93.60],
        "Abdomen": [83],
        "Hip": [98.7],
        "Thigh": [58.7],
        "Knee": [37.3],
        "Ankle": [23.4],
        "Biceps": [30.5],
        "Forearm": [28.9],
        "Wrist": [18.2],
        "Bmi": [23.33],
        "ACratio": [0.886752],
        "HTratio": [1.681431]
    }

    body_stats_df = pd.DataFrame(data=body_stats)
    body_stats_df = transformer.transform(body_stats_df)

    density = model.predict(body_stats_df)
    fat = ((4.95/density) - 4.5)*100

    context = {
        "density": round(density[0], 2),
        "fat": round(fat[0], 2)
    }

    return render(request, 'dashboard/bodystats.html', context=context)
