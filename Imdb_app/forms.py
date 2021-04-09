
from django import forms
from Imdb_app.models import ApplicationUser, Comment_model


class SignupForm(forms.Form):
    display_name = forms.CharField(max_length=50)
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
    # Was unsure of to whether to include the likes,want_to_see, and have_seen in the inital signup or rather after


# This is the comment form **Model Form
class Comment_Form(forms.ModelForm):
    class Meta:
        Model = Comment_model
        fields = [
            'input_field',
            'movie',
            'commenter',
            'date_created',
            'recommended'
        ]


class SearchForm(forms.Form):
    search_selection = forms.CharField(max_length=180)
