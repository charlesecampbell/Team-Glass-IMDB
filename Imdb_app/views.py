from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, logout, authenticate
from Imdb_app.forms import SearchForm, SignupForm, Comment_Form, LoginForm
from Imdb_app.models import ApplicationUser, Comment_model
from django.views import View
from Imdb_app.api_search_call import search_bar, results_data
import requests

# Error handling


def error_404(request, exception):
    return render(request, "404.html")


def error_500(request):
    return render(request, "500.html")

# Create your views here.


def home_page_view(request):
    context = {}
    user = request.user
    # SEARCH FORM IN THE HEADER
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():

            # This is the search request data
            data = search_form.cleaned_data

            # This calls the helper function to make the api Call
            reply = search_bar(data['search_actors_or_movies'])

            # This will tell us if its an actor or other media and
            # help the redirection
            page_decision = reply['d'][0]['id'][:2]

            # This runs the data collecter function and creates a list of
            # dictionaries to access in the templates
            movie_info = results_data(reply)

            # This allows access to the data to be used in different views
            # (see search_details_view to see how to call it)
            request.session['movie_info'] = movie_info

            # This directs the search results to the correct page
            if page_decision != 'nm':
                return redirect(reverse('search_details'))
            else:
                return redirect(reverse('actorspage'))
    # END SEARCH FORM IN THE HEADER

    search_form = SearchForm()
    context.update({'search_form': search_form, 'user': user})
    return render(request, 'homepage.html', context)


class SignupView(View):
    form_class = SignupForm
    search_form = SearchForm
    template_name = "signup.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {
            "form": form,
            "header": "Signup"
        })

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
        return render(request, self.template_name, {
            "form": form,
            "header": "Signup"
        })


def search_details_view(request):
    # Gets the info collected from the api request
    movie_info = request.session.get('movie_info')

    # Same as in the home page view this should go in every view as
    # it controls the header search bar
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            data = search_form.cleaned_data
            print(data['search_actors_or_movies'])
            reply = search_bar(data['search_actors_or_movies'])
            page_decision = reply['d'][0]['id'][:2]
            movie_info = results_data(reply)
            request.session['movie_info'] = movie_info
            if page_decision != 'nm':
                return redirect(reverse('search_details'))
            else:
                return redirect(reverse('actorspage'))
    # END HEADER SEARCH BAR
    search_form = SearchForm()
    return render(request, 'search_details.html', {
        'search_form': search_form,
        'movie_info': movie_info
    })


# Details page view where as of now it has dummy data but will
# eventually be filled with actual data from api
def details_page(request, selection_id):
    print(selection_id)
    context = {}

    # SEARCH FORM IN THE HEADER
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            data = search_form.cleaned_data
            reply = search_bar(data['search_actors_or_movies'])
            page_decision = reply['d'][0]['id'][:2]
            movie_info = results_data(reply)
            request.session['movie_info'] = movie_info
            if page_decision != 'nm':
                return redirect(reverse('search_details'))
            else:
                return redirect(reverse('actorspage'))
    # End of Form Search Request From Header

    movie = {
        'title': 'Test Film',
        'description': '''Lorem ipsum dolor sit amet, consectetur adipiscing
        elit. Ut ultricies augue eu nisi mollis, dapibus consectetur neque
        eleifend. Praesent sit amet dui tincidunt, condimentum quam sit amet,
        malesuada nisl. Integer ac nisi aliquet nunc dignissim varius.
        Suspendisse eu ante sit amet nisi facilisis aliquam. Duis efficitur
        scelerisque lacinia. Nulla commodo tortor tristique mi luctus, vel
        ornare enim cursus. Praesent porttitor ac augue bibendum venenatis.
        Vivamus lacus lorem, dapibus sit amet feugiat non, feugiat nec mauris.
        Ut lorem sem, elementum scelerisque risus sed, mattis porta felis.
        Interdum et malesuada fames ac ante ipsum primis in faucibus.
        Donec sed nulla at tellus luctus maximus. Suspendisse convallis urna
        eget mauris tincidunt laoreet. Nam suscipit nisi vel mauris ornare
        sodales. Nullam bibendum faucibus congue. Curabitur at felis libero.'''
    }
    context.update({'movie': movie})
    if request.method == 'POST':
        form = Comment_Form(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_item = Comment_model.objects.create(
                input_field=data['input_field'],
                movie=data['movie'],
                commenter=request.user,
                recommended=data['recommended']
            )
            print(new_item)
    form = Comment_Form()
    search_form = SearchForm()
    context.update(
        {
            'form': form,
            'selection_id': selection_id,
            'search_form': search_form
        })
    return render(request, 'details_page.html', context)


def login_view(request):
    context = {}

    # SEARCH FORM IN THE HEADER
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            data = search_form.cleaned_data
            reply = search_bar(data['search_actors_or_movies'])
            page_decision = reply['d'][0]['id'][:2]
            movie_info = results_data(reply)
            request.session['movie_info'] = movie_info
            if page_decision != 'nm':
                return redirect(reverse('search_details'))
            else:
                return redirect(reverse('actorspage'))
    # End of Form Search Request From Header

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, username=data['username'],
                password=data['password']
            )
            if user:
                login(request, user)
                return redirect(reverse('home'))
    form = LoginForm()
    search_form = SearchForm()
    context.update({'form': form, 'search_form': search_form})
    return render(request, 'login.html', context)


def logout_view(request):
    logout(request)
    return redirect(reverse('home'))


def ActorsView(request):
    context = {}
    reply = {}

    # SEARCH FORM IN THE HEADER
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            data = search_form.cleaned_data
            reply = search_bar(data['search_actors_or_movies'])
            page_decision = reply['d'][0]['id'][:2]
            movie_info = results_data(reply)
            request.session['movie_info'] = movie_info
            if page_decision != 'nm':
                return redirect(reverse('search_details'))
            else:
                return redirect(reverse('actorspage'))
    # End of Form Search Request From Header

    movie_info = request.session.get("movie_info")
    search_id = movie_info[0]['id']

    # Api Call With the Search Results
    url = "https://imdb8.p.rapidapi.com/actors/get-all-images"
    querystring = {"nconst": search_id}

    headers = {
        'x-rapidapi-key': "a3d8d2b4e0msh9912babc2875bfcp1e811cjsn1489c4504884",
        'x-rapidapi-host': "imdb8.p.rapidapi.com"
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)

    reply = response.json()
    search_form = SearchForm()
    count = 0
    imageArray = []
    for images in reply['resource']['images']:
        if count < 5:
            imageArray.append(images['url'])
            count += 1
    context.update(
        {
            'reply': reply,
            'imageArray': imageArray,
            'movie_info': movie_info,
            'search_form': search_form
            })
    return render(request, 'actorspage.html', context)
