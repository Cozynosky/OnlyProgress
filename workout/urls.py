from django.urls import path
from . import views


app_name = "workout"
urlpatterns = [
    path("", views.exercises_view, name="exercises"),
    path("train_with_ai/<int:exercise_id>/<int:reps>", views.train_with_ai_view, name="train_with_ai"),
    path("add_training/<int:exercise_id>/", views.add_training_view, name="add_training"),
    path("exercise_history/<int:exercise_id>/<int:page>/", views.exercise_history_view, name="exercise_history"),
    path("camera_feed/<int:exercise_id>/<int:reps>/", views.camera_feed, name="camera_feed")
]