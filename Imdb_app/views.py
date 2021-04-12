from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, logout
import requests
from requests.api import request
from Imdb_app.forms import SearchForm, SignupForm
from Imdb_app.models import ApplicationUser
from django.views import View
# Create your views here.


def home_page_view(request):
    context = {}
    reply = {}
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(data['search_selection'])
            # Api Call With the Search Results
            url = "https://imdb8.p.rapidapi.com/auto-complete"
            querystring = {"q": data['search_selection']}

            headers = {
                'x-rapidapi-key': "1ddf0a8da3msh877010e622bf74dp10873cjsnd762a292965a",
                'x-rapidapi-host': "imdb8.p.rapidapi.com"
            }

            response = requests.request(
                "GET", url, headers=headers, params=querystring)

            reply = response.json()
            imageUrl = reply['d'][0]['i']['imageUrl']
            print(response.json())
    form = SearchForm()
    context.update({'form': form, 'reply': reply, 'imageUrl': imageUrl})
    return render(request, 'homepage.html', context)


class SignupView(View):
    form_class = SignupForm
    template_name = "signup.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form, "header": "Signup"})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = ApplicationUser.objects.create_user(
                username=data.get("username"),
                display_name=data.get("display_name"),
                password=data.get("password")
            )
            login(request, user)
            return redirect(reverse("home"))
        return render(request, self.template_name, {"form": form, "header": "Signup"})


def ActorsView(request):
    context = {}
    reply = {}
    movie_info = request.session.get("movie_info")
# Api Call With the Search Results
    url = "https://imdb8.p.rapidapi.com/actors/get-all-images"
    querystring = {"q": movie_info['d'][0]['id']}

    headers = {
        'x-rapidapi-key': "a3d8d2b4e0msh9912babc2875bfcp1e811cjsn1489c4504884",
        'x-rapidapi-host': "imdb8.p.rapidapi.com"
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)

    reply = response.json()
    imageUrl = movie_info['d'][0]['i']['imageUrl']
    print(response.json())
    context.update({'form': form, 'reply': reply, 'imageUrl': imageUrl})
    return render(request, 'actorspage.html', context)
