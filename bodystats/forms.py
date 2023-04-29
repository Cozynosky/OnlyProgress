from django import forms
from .models import BodyStats


class BodystatsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, value in self.fields.items():
            value.widget.attrs['placeholder'] = value.help_text
    
    class Meta:
        model = BodyStats
        fields = ["date", "age", "weight", "height", "neck", "chest", "abdomen", "hip", "thigh", "knee", "ankle", "biceps", "forearm", "wrist"]
        widgets = {
            "date": forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }
