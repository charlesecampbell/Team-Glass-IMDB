
from django import forms
from Imdb_app.models import Comment_model


class SignupForm(forms.Form):
    email = forms.EmailField()
    display_name = forms.CharField(max_length=50)
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
    # Was unsure of to whether to include the likes,want_to_see,
    # and have_seen in the inital signup or rather after


# This is the comment form **Model Form
class Comment_Form(forms.ModelForm):
    class Meta:
        model = Comment_model
        fields = [
            'input_field',
            'recommended'
        ]


class SearchForm(forms.Form):
    search_actors_or_movies = forms.CharField(
        label='',
        max_length=180,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search Actors or Movies'
            })
        )


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
