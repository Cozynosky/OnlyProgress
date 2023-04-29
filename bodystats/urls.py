from django.urls import path
from . import views


app_name = "bodystats"
urlpatterns = [
    path("", views.latest_bodystats_view, name="show_latest"),
    path("show_bodystats/<int:id>/", views.show_bodystats_view, name="show_bodystats"),
    path("add_bodystats/<str:fill>", views.add_bodystats_view, name="add_bodystats"),
    path("history/page/<int:page>", views.history_bodystats_view, name="show_history"),
    path("update_bodystats/<int:id>", views.update_bodystats_view, name="update_bodystats"),
    path("delete_bodystats/<int:id>", views.delete_bodystats_view, name="delete_bodystats")
]