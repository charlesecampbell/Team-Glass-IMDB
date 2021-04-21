from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from Imdb_app.forms import SearchForm, SignupForm, Comment_Form, LoginForm
from Imdb_app.forms import UpdateUserForm
from Imdb_app.models import ApplicationUser, Comment_model, LikedMoviesModel
from Imdb_app.models import WantToSeeModel, HaveSeenModel
from django.views import View
from django.views.generic.base import TemplateView
from Imdb_app.helpers import *
from Imdb_app.helpers import retrieve_movie_trailer_id
from Imdb_app.api_search_call import top_movie_data
from Imdb_app.api_search_call import top_tv_info, hollywood_news
from Imdb_app.api_search_call import run_search
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

    # it controls the header search bar
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        reply_data = run_search(request, search_form)
        movie_info = reply_data[0]
        page_decision = reply_data[1]
        request.session['movie_info'] = (movie_info)
        if page_decision != 'nm':
            return redirect(reverse('search_details'))
        else:
            return redirect(reverse('actorspage'))
    # END HEADER SEARCH BAR

    # GETS TOP FIVE MOVIES
    movie_data = top_movie_data()

    # GETS TOP FIVE TV SHOWS
    tv_data = top_tv_info()

    # top Tv Data
    top_news = hollywood_news()

    search_form = SearchForm()
    context.update({
        'search_form': search_form,
        'user': user,
        'home_page_movie_data': movie_data,
        'homepage_tv_data': tv_data,
        'comments': comments,
        'top_news': top_news
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
            print(request.user.id)
            return redirect(reverse("login"))
        return render(request, self.template_name, {
            "form": form,
            "header": "Signup"
        })


def search_details_view(request):

    # Gets the info collected from the api request
    movie_info = request.session.get('movie_info')
    context = {}

    # it controls the header search bar
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        reply_data = run_search(request, search_form)
        movie_info = reply_data[0]
        page_decision = reply_data[1]
        request.session['movie_info'] = (movie_info)
        if page_decision != 'nm':
            return redirect(reverse('search_details'))
        else:
            return redirect(reverse('actorspage'))
    # END HEADER SEARCH BAR

    search_form = SearchForm()
    context.update({
        'search_form': search_form,
        'movie_info': movie_info,
    })
    return render(request, 'search_details.html', context)


# Details page view
def details_page(request, selection_id):

    if 'search_actors_or_movies' in request.POST:
        if request.method == 'POST':
            search_form = SearchForm(request.POST)
            reply_data = run_search(request, search_form)
            movie_info = reply_data[0]
            page_decision = reply_data[1]
            request.session['movie_info'] = (movie_info)
            if page_decision != 'nm':
                return redirect(reverse('search_details'))
            else:
                return redirect(reverse('actorspage'))
    # END HEADER SEARCH BAR

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
    # Find Five Recommendations
    recommendations = find_recommendations(selection_id)
    context.update({'recommendations': recommendations})

    # Get plot of movie
    plot = find_movie_plot(selection_id)
    context.update({'plot': plot['plots'][0]['text']})
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
                recommended=data['recommended'],
                user_image=f'/media/{request.user.user_image}'
            )
            # print(new_item)
    comments = Comment_model.objects.filter(movie_id=selection_id)
    form = Comment_Form()
    search_form = SearchForm()
    context.update(
        {
            'form': form,
            'selection_id': selection_id,
            'search_form': search_form,
            'trailer_link': movie_trailer[0],
            'encode_type': movie_trailer[1],
            'comments': comments,
        })
    print(context)
    return render(request, 'details_page.html', context)


class UserProfileView(TemplateView):
    template_name = "userprofile.html"

    def get_context_data(self, applicationuser_id):
        context = super().get_context_data()
        context['haveseen'] = HaveSeenModel.objects.all().filter(
            user=applicationuser_id)
        context['wanttosee'] = WantToSeeModel.objects.all().filter(
            user=applicationuser_id
        )
        context['comments'] = Comment_model.objects.all().filter(
            commenter=applicationuser_id
        ).order_by('date_created').reverse()
        context['search'] = SearchForm()
        context['my_user'] = ApplicationUser.objects.all().filter(
            id=applicationuser_id
        )
        return context


def login_view(request):
    context = {}

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
    context.update({'form': form})
    return render(request, 'login.html', context)


class LogoutView(TemplateView):
    def get(self, request):
        logout(request)
        return redirect(reverse('login'))


def ActorsView(request):
    context = {}
    reply = ''
    search_form = SearchForm()

    # it controls the header search bar
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        reply_data = run_search(request, search_form)
        movie_info = reply_data[0]
        page_decision = reply_data[1]
        request.session['movie_info'] = (movie_info)
        if page_decision != 'nm':
            return redirect(reverse('search_details'))
        else:
            return redirect(reverse('actorspage'))
    # END HEADER SEARCH BAR

    movie_info = request.session.get("movie_info")

    # Api Call For Images
    url = "https://imdb8.p.rapidapi.com/actors/get-all-images"
    querystring = {"nconst": movie_info[0]['id']}
    headers = {
        'x-rapidapi-key': config('MAIN_IMDB_KEY'),
        'x-rapidapi-host': "imdb8.p.rapidapi.com"
    }
    response = requests.request(
        "GET", url, headers=headers, params=querystring)
    reply_data = response.json()
    count = 0
    imageArray = []
    for images in reply_data["resource"]['images']:
        if count < 5:
            imageArray.append(images['url'])
            count += 1

    # Api Call With the Bio Results
    url = "https://imdb8.p.rapidapi.com/actors/get-bio"
    querystring = {"nconst": movie_info[0]['id']}
    headers = {
        'x-rapidapi-key': config('MAIN_IMDB_KEY'),
        'x-rapidapi-host': "imdb8.p.rapidapi.com"
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)

    reply = response.json()
    actor_image = reply["image"]["url"]
    actor_bio = reply["miniBios"][0]["text"]
    actor_birthdate = reply["birthDate"]
    actor_birthplace = reply["birthPlace"]
    name = reply["name"]

    # API Call with the Actors Award Results
    url = "https://imdb8.p.rapidapi.com/actors/get-awards"

    querystring = {"nconst": movie_info[0]['id']}

    headers = {
        'x-rapidapi-key': config('MAIN_IMDB_KEY'),
        'x-rapidapi-host': "imdb8.p.rapidapi.com"
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)

    award_reply = response.json()
    won = award_reply["resource"]["awards"]
    won_list = []
    for award in won:
        if "category" in award:
            if award["isWinner"]:
                won_list.append({
                    "awardName": award["awardName"],
                    "category": award["category"],
                    "year": award["year"],
                    "eventName": award["eventName"],
                })

    context.update(
        {
            'search_form': search_form,
            'imageArray': imageArray,
            'movie_info': movie_info,
            'actor_image': actor_image,
            'actor_bio': actor_bio,
            'actor_birthdate': actor_birthdate,
            'actor_birthplace': actor_birthplace,
            'name': name,
            'won_list': won_list,
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


@login_required
def profile_update(request, applicationuser_id):
    if request.method == 'POST':
        user_form = UpdateUserForm(
            request.POST, request.FILES, instance=request.user)
        if user_form.is_valid():
            user_form.cleaned_data
            user_form.save()
            return redirect(f'/user/{applicationuser_id}/')
    else:
        user_form = UpdateUserForm(initial={
            "display_name": request.user.display_name,
            "email": request.user.email,
            "bio": request.user.bio,
            "user_image": request.user.user_image
        })
    return render(request, 'update_user.html', {'userform': user_form})
