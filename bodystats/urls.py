from django.urls import path
from . import views


app_name = "bodystats"
urlpatterns = [
    path("", views.latest_bodystats_view, name="show_latest"),
    path("<int:id>/", views.show_bodystats_view, name="show_bodystats"),
    path("add_bodystats/", views.add_bodystats_view, name="add_bodystats")
]