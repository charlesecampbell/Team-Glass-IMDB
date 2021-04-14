from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, logout, authenticate
from Imdb_app.forms import SearchForm, SignupForm, Comment_Form, LoginForm
from Imdb_app.models import ApplicationUser, Comment_model, LikedMoviesModel
from Imdb_app.models import WantToSeeModel, HaveSeenModel
from django.views import View
from Imdb_app.helpers import check_model, check_model_x_api
from Imdb_app.helpers import retrieve_movie_trailer_id
from Imdb_app.api_search_call import search_bar, results_data, top_movie_data
from Imdb_app.api_search_call import top_tv_info
from decouple import config
import requests


# Error handling
def error_404(request, exception):
    return render(request, "404.html")


def error_500(request):
    return render(request, "500.html")


# Create your views here.
def home_page_view(request):
    comments = Comment_model.objects.all().order_by('date_created').reverse()
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

    # GETS TOP FIVE MOVIES
    movie_data = top_movie_data()

    # GETS TOP FIVE TV SHOWS
    tv_data = top_tv_info()

    search_form = SearchForm()
    context.update({
        'search_form': search_form,
        'user': user,
        'home_page_movie_data': movie_data,
        'homepage_tv_data': tv_data,
        'comments': comments
        })
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


# Details page view
def details_page(request, selection_id):

    # HEADER FORM SEARCH BAR REQUEST
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

    app_user = ApplicationUser.objects.filter(
        username=request.user.username).first()

    liked = check_model(app_user, LikedMoviesModel, selection_id)
    seen = check_model(app_user, HaveSeenModel, selection_id)
    want_to = check_model(app_user, WantToSeeModel, selection_id)
    '''I have here my api keys but it can be changed to whichever we use'''
    url = "https://imdb8.p.rapidapi.com/auto-complete"

    querystring = {"q": selection_id}

    headers = {
        'x-rapidapi-key': config('MAIN_IMDB_KEY'),
        'x-rapidapi-host': "imdb8.p.rapidapi.com"
    }

    response = requests.request(
        "GET",
        url,
        headers=headers,
        params=querystring
        )
    reply_data = response.json()
    context = {}
    context.update({'reply_data': reply_data})
    check_model_x_api(liked, context['reply_data'], 'liked_movie')
    check_model_x_api(seen, context['reply_data'], 'seen_movie')
    check_model_x_api(want_to, context['reply_data'], 'want_to_see')
    print(context)

    # FETCHES THE MOVIE TRAILER IF THERE IS ONE, SOMETIMES THERE ISNT A MATCH
    movie_id = reply_data['d'][0]['id']
    movie_trailer = retrieve_movie_trailer_id(movie_id)
    # END TRAILER FETCH

    if request.method == 'POST':
        form = Comment_Form(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_item = Comment_model.objects.create(
                input_field=data['input_field'],
                movie_image=reply_data['d'][0]['i']['imageUrl'],
                movie_title=reply_data['d'][0]['l'],
                commenter=request.user,
                movie_id=selection_id,
                recommended=data['recommended']
            )
            print(new_item)
    form = Comment_Form()
    search_form = SearchForm()
    context.update(
        {
            'form': form,
            'selection_id': selection_id,
            'search_form': search_form,
            'trailer_link': movie_trailer[0],
            'encode_type': movie_trailer[1]
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
        'x-rapidapi-key': config('MAIN_IMDB_KEY'),
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


# View To add Movie to likes
def add_to_likes(request, id):
    '''want to potentially check our other models if their is a movie linked
    with the user and then delete from other model instance and create new'''
    app_user = ApplicationUser.objects.filter(
        username=request.user.username).first()

    url = "https://imdb8.p.rapidapi.com/auto-complete"

    querystring = {"q": id}

    headers = {
        'x-rapidapi-key': config('MAIN_IMDB_KEY'),
        'x-rapidapi-host': "imdb8.p.rapidapi.com"
    }

    response = requests.request(
        "GET",
        url,
        headers=headers,
        params=querystring
        )

    data = response.json()
    title = data['d'][0]['l']
    img = data['d'][0]['i']['imageUrl']
    year = data['d'][0]['y']
    LikedMoviesModel.objects.create(
        movie_title=title,
        movie_img=img,
        movie_release=year,
        movie_actors=data['d'][0]['s'],
        movie_id=id,
        user=app_user
    )
    return redirect(f'/details/{id}')


# View to add movie to want_to_see
def want_to_see(request, id):
    '''want to potentially check our other models if their is a movie linked
    with the user and then delete from other model instance and create new'''
    app_user = ApplicationUser.objects.filter(
        username=request.user.username).first()

    url = "https://imdb8.p.rapidapi.com/auto-complete"

    querystring = {"q": id}

    headers = {
        'x-rapidapi-key': config('MAIN_IMDB_KEY'),
        'x-rapidapi-host': "imdb8.p.rapidapi.com"
    }

    response = requests.request(
        "GET",
        url,
        headers=headers,
        params=querystring
        )
    data = response.json()
    title = data['d'][0]['l']
    img = data['d'][0]['i']['imageUrl']
    year = data['d'][0]['y']
    WantToSeeModel.objects.create(
        movie_title=title,
        movie_img=img,
        movie_release=year,
        movie_actors=data['d'][0]['s'],
        movie_id=id,
        user=app_user
    )
    return redirect(f'/details/{id}')


# View to add movei to have seen
def movies_have_seen(request, id):
    '''want to potentially check our other models if their is a movie linked
    with the user and then delete from other model instance and create new'''
    app_user = ApplicationUser.objects.filter(
        username=request.user.username).first()

    want_to = check_model(app_user, WantToSeeModel, id)
    if want_to is not None:
        WantToSeeModel.objects.filter(movie_id=want_to).first().delete()
    url = "https://imdb8.p.rapidapi.com/auto-complete"

    querystring = {"q": id}

    headers = {
        'x-rapidapi-key': config('MAIN_IMDB_KEY'),
        'x-rapidapi-host': "imdb8.p.rapidapi.com"
    }

    response = requests.request(
        "GET",
        url,
        headers=headers,
        params=querystring
        )
    data = response.json()
    title = data['d'][0]['l']
    img = data['d'][0]['i']['imageUrl']
    year = data['d'][0]['y']
    HaveSeenModel.objects.create(
        movie_title=title,
        movie_img=img,
        movie_release=year,
        movie_actors=data['d'][0]['s'],
        movie_id=id,
        user=app_user
    )
    return redirect(f'/details/{id}')
