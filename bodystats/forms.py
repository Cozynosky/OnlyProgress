from django import forms
from .models import BodyStats


class NewBodystatsForm(forms.ModelForm):
    class Meta:
        model = BodyStats
        fields = ["date", "age", "weight", "height", "neck", "chest", "abdomen", "hip", "thigh", "knee", "ankle", "biceps", "forearm", "wrist"]
        widgets = {
            "date": forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }
