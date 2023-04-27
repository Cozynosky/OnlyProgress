from django.urls import path

from . import views


app_name = "profile"
urlpatterns = [
    path("login/", views.login_user, name="login_user"),
    path("register/", views.register_user, name="register_user"),
    path("logout/", views.logout_user, name="logout_user"),
    path("dashboard/home", views.dashboard_home, name="dashboard_home"),
    path("dashboard/bodystats", views.dashboard_bodystats, name="dashboard_bodystats")
]