from django.urls import path
from . import views


app_name = "predictions"
urlpatterns = [
    path("face_analysis/", views.face_analysis_view, name="face_analysis"),
    path("face_analysis/camera_feed/", views.camera_feed, name="camera_feed")
]