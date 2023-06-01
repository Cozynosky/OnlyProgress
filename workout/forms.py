from django import forms
from .models import Workout


class WorkoutForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, value in self.fields.items():
            value.widget.attrs['placeholder'] = value.help_text
    
    class Meta:
        model = Workout
        fields = ["date", "reps"]
        widgets = {
            "date": forms.DateInput(attrs={'type': 'date'})
        }