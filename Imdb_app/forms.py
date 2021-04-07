from django import forms
from Imdb_app.models import ApplicationUser


class SignupForm(forms.Form):
    username = forms.CharField(max_length=140)
    password = forms.CharField(widget=forms.PasswordInput)
    # email = forms.EmailField()
