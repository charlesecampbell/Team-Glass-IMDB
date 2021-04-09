from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, logout, authenticate
import requests
from Imdb_app.forms import SearchForm, SignupForm, Comment_Form, LoginForm
from Imdb_app.models import ApplicationUser, Comment_model
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
                email=data.get("email"),
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

# Details page view where as of now it has dummy data but will eventually be filled with actual data from api
def details_page(request):
    context = {}
    movie = {
        'title' : 'Test Film',
        'description' : '''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut ultricies augue eu nisi mollis, dapibus consectetur neque eleifend. Praesent sit amet dui tincidunt, condimentum quam sit amet, malesuada nisl. 
        Integer ac nisi aliquet nunc dignissim varius. Suspendisse eu ante sit amet nisi facilisis aliquam. Duis efficitur scelerisque lacinia. Nulla commodo tortor tristique mi luctus, vel ornare enim cursus. 
        Praesent porttitor ac augue bibendum venenatis. Vivamus lacus lorem, dapibus sit amet feugiat non, feugiat nec mauris. Ut lorem sem, elementum scelerisque risus sed, mattis porta felis. Interdum et malesuada fames ac ante ipsum primis in faucibus. 
        Donec sed nulla at tellus luctus maximus. Suspendisse convallis urna eget mauris tincidunt laoreet. Nam suscipit nisi vel mauris ornare sodales. Nullam bibendum faucibus congue. Curabitur at felis libero.'''
    }
    context.update({'movie': movie})
    if request.method == 'POST':
        form = Comment_Form(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_item = Comment_model.objects.create(
                input_field = data['input_field'],
                movie = data['movie'],
                commenter = request.user,
                recommended = data['recommended']
            )
            print(new_item)
    form = Comment_Form()
    context.update({'form': form})
    return render(request, 'details_page.html', context)

def login_view(request):
    context = {}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])
            if user:
                login(request,user)
                print('logged in')
    form = LoginForm()
    context.update({'form': form})
    return render(request, 'login.html', context)