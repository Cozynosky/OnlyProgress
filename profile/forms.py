from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    sex = forms.ChoiceField(label="Sex", choices=((1, "Man"), (0, "Woman")))

    class Meta:
        model = User
        fields = ("first_name", "last_name", "sex", "username", "email", "password1", "password2")
    
    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            user.profile.sex = self.cleaned_data["sex"]
        return user
