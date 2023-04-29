from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from profile.models import Profile


class BodyStats(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateTimeField(help_text="Date of measurement")
    age = models.IntegerField(help_text="Age in years", validators=[MinValueValidator(18), MaxValueValidator(99)])
    weight = models.DecimalField(help_text="Body mass in kg", max_digits=4, decimal_places=1, validators=[MinValueValidator(40), MaxValueValidator(200)])
    height = models.DecimalField(help_text="Body height in cm", max_digits=4, decimal_places=1, validators=[MinValueValidator(150), MaxValueValidator(220)])
    neck = models.DecimalField(help_text="Circumference in cm", max_digits=3, decimal_places=1, validators=[MinValueValidator(20), MaxValueValidator(60)])
    chest = models.DecimalField(help_text="Circumference in cm", max_digits=4, decimal_places=1, validators=[MinValueValidator(60), MaxValueValidator(140)])
    abdomen = models.DecimalField(help_text="Circumference in cm", max_digits=4, decimal_places=1, validators=[MinValueValidator(50), MaxValueValidator(150)])
    hip = models.DecimalField(help_text="Circumference in cm", max_digits=4, decimal_places=1, validators=[MinValueValidator(80), MaxValueValidator(130)])
    thigh = models.DecimalField(help_text="Circumference in cm", max_digits=3, decimal_places=1, validators=[MinValueValidator(40), MaxValueValidator(80)])
    knee = models.DecimalField(help_text="Circumference in cm", max_digits=3, decimal_places=1, validators=[MinValueValidator(26), MaxValueValidator(55)])
    ankle = models.DecimalField(help_text="Circumference in cm", max_digits=3, decimal_places=1, validators=[MinValueValidator(14), MaxValueValidator(35)])
    biceps = models.DecimalField(help_text="Circumference in cm", max_digits=3, decimal_places=1, validators=[MinValueValidator(20), MaxValueValidator(50)])
    forearm = models.DecimalField(help_text="Circumference in cm", max_digits=3, decimal_places=1, validators=[MinValueValidator(18), MaxValueValidator(38)])
    wrist = models.DecimalField(help_text="Circumference in cm", max_digits=3, decimal_places=1, validators=[MinValueValidator(11), MaxValueValidator(25)])
    bmi = models.DecimalField(help_text="Body mass index", max_digits=4, decimal_places=2, validators=[MinValueValidator(5), MaxValueValidator(60)])
    bodyfat = models.DecimalField(help_text="Bodyfat %", max_digits=4, decimal_places=2)
    
    class Meta:
        ordering = ["date"]
        
    def __str__(self) -> str:
        return f"Stats measured at {self.date}"
    
    
    