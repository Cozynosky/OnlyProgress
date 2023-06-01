from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from profile.models import Profile
from .pose import BodyPart

    
class Exercise(models.Model):
    name = models.CharField(help_text="Exercise name", max_length=50)
    desc = models.CharField(help_text="Exercise description",max_length=250)
    bodypart_a = models.IntegerField(help_text="Bodypart A name", choices=((item[1], item[0]) for item in BodyPart.items()))
    bodypart_b = models.IntegerField(help_text="Bodypart B name", choices=((item[1], item[0]) for item in BodyPart.items()))
    bodypart_c = models.IntegerField(help_text="Bodypart C name", choices=((item[1], item[0]) for item in BodyPart.items()))
    start_angle = models.IntegerField(help_text="Starting angle", validators=[MinValueValidator(0), MaxValueValidator(360)])
    end_angle = models.IntegerField(help_text="Ending angle", validators=[MinValueValidator(0), MaxValueValidator(360)])
    img_url = models.URLField(max_length = 200)
    
    def __str__(self) -> str:
        return f"{self.name}"
    
class Workout(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateField(help_text="Training date")
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    reps = models.IntegerField(help_text="Exercise reps", default=1)
    sets = models.IntegerField(help_text="Exercise sets", default=1)