from django.urls import path
from . import views


app_name = "workout"
urlpatterns = [
    path("", views.workout_view, name="workout"),
    path("camera_feed/", views.camera_feed, name="camera_feed")
]