
from django import forms
from Imdb_app.models import Comment_model, ApplicationUser


class SignupForm(forms.Form):
    email = forms.EmailField(
        label='',
        widget=forms.TextInput(attrs={
            'placeholder': 'Email'
        })
    )
    display_name = forms.CharField(
        label='',
        max_length=50,
        widget=forms.TextInput(attrs={
            'placeholder': 'Display Name'
        }))
    username = forms.CharField(
        label='',
        max_length=50,
        widget=forms.TextInput(attrs={
            'placeholder': 'Username'
        }))
    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password'
        }))


# This is the comment form **Model Form
class Comment_Form(forms.ModelForm):
    input_field = forms.CharField(
        label='', widget=forms.Textarea(
            attrs={'placeholder': 'Comment or Review'}))

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
    username = forms.CharField(
        label='',
        max_length=50,
        widget=forms.TextInput(attrs={
            'placeholder': 'Username'
        }))
    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password'
        }))


class UpdateUserForm(forms.ModelForm):
    display_name = forms.CharField(
        label='', widget=forms.TextInput(
            attrs={'placeholder': 'Display Name'}))
    email = forms.EmailField(
        label='', widget=forms.EmailInput(
            attrs={'placeholder': 'Email'}))
    bio = forms.CharField(label='', widget=forms.Textarea(
        attrs={'placeholder': 'About Me'}))
    user_image = forms.FileField(label='')

    class Meta:
        model = ApplicationUser
        fields = [
            'display_name',
            'email',
            'bio',
            'user_image'
        ]
