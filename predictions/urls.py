from django.urls import path
from . import views


app_name = "predictions"
urlpatterns = [
    path("", views.face_analysis_view, name="face_analysis"),

]