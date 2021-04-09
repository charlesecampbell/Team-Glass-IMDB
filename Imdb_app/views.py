from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, logout
import requests
from Imdb_app.forms import SearchForm, SignupForm
from Imdb_app.models import ApplicationUser
from django.views import View
# Create your views here.


def home_page_view(request):
    context = {}
    reply = {}
    imageUrl = ''
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            data = search_form.cleaned_data
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
            page_decision = reply['d'][0]['id'][:2]
            # This directs the search results to the search results page
            if page_decision is not 'nm': 
                imageUrl = reply['d'][0]['i']['imageUrl']

                movie_info = []
                for poster in reply['d']:
                    movie_info.append({'poster': poster['i']['imageUrl'], 'id': poster['id'], 'year': poster['y'], 'title': poster['l']}) 
                return render(request, 'search_details.html', {'imageUrl': imageUrl, 'movie_info': movie_info})

            
    search_form = SearchForm()
    context.update({'search_form': search_form, 'reply': reply, 'imageUrl': imageUrl})
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


def search_details_view(request):

    context = {}
    reply = {}
    imageUrl = ''
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            data = search_form.cleaned_data
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
            page_decision = reply['d'][0]['id'][:2]
            if page_decision is not 'nm':
                return redirect(reverse("search_details"))
    return render(request, 'search_details.html')
