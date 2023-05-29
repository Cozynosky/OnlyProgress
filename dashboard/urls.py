from django.urls import path, include
from . import views

app_name = "dashboard"
urlpatterns = [
    path("", views.dashboard_home, name="home"),
    path('bodystats/', include("bodystats.urls", namespace="bodystats")),
    path('face-analysis/', include("predictions.urls", namespace="predictions")),
    path('workout/', include("workout.urls", namespace="workout"))
]