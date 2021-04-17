from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, logout, authenticate
from Imdb_app.forms import SearchForm, SignupForm, Comment_Form, LoginForm
from Imdb_app.models import ApplicationUser, Comment_model, LikedMoviesModel
from Imdb_app.models import WantToSeeModel, HaveSeenModel
from django.views import View
from django.views.generic.base import TemplateView
from Imdb_app.helpers import check_model, check_model_x_api
from Imdb_app.helpers import retrieve_movie_trailer_id
from Imdb_app.api_search_call import search_bar, results_data, top_movie_data
from Imdb_app.api_search_call import top_tv_info, hollywood_news
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
            request.session['movie_info'] = (movie_info)
            # This directs the search results to the correct page
            if page_decision != 'nm':
                return redirect(reverse('search_details'))
            else:
                return redirect(reverse('actorspage'))
    # END SEARCH FORM IN THE HEADER

    # GETS TOP FIVE MOVIES
    # movie_data = top_movie_data()
    movie_data = [{'id': 'tt5034838', 'image': 'https://m.media-amazon.com/images/M/MV5BZmYzMzU4NjctNDI0Mi00MGExLWI3ZDQtYzQzYThmYzc2ZmNjXkEyXkFqcGdeQXVyMTEyMjM2NDc2._V1_.jpg', 'title': 'Godzilla vs. Kong', 'year': 2021, 'plot': 'The epic next chapter in the cinematic Monsterverse pits two of the greatest icons in motion picture history against one another - the fearsome Godzilla and the mighty Kong - with humanity caught in the balance.'}, {'id': 'tt3480822', 'image': 'https://m.media-amazon.com/images/M/MV5BYjdmODAzNTctNWU1NS00ZmRiLWFiM2YtMjAyNzgzZWJlZjhlXkEyXkFqcGdeQXVyMTEyMjM2NDc2._V1_.jpg', 'title': 'Black Widow', 'year': 2021, 'plot': 'A film about Natasha Romanoff in her quests between the films Civil War and Infinity War.'}, {'id': 'tt12361974', 'image': 'https://m.media-amazon.com/images/M/MV5BYjI3NDg0ZTEtMDEwYS00YWMyLThjYjktMTNlM2NmYjc1OGRiXkEyXkFqcGdeQXVyMTEyMjM2NDc2._V1_.jpg', 'title': "Zack Snyder's Justice League", 'year': 2021, 'plot': "Determined to ensure Superman's ultimate sacrifice was not in vain, Bruce Wayne aligns forces with Diana Prince with plans to recruit a team of metahumans to protect the world from an approaching threat of catastrophic proportions."}, {'id': 'tt0293429', 'image': 'https://m.media-amazon.com/images/M/MV5BY2ZlNWIxODMtN2YwZi00ZjNmLWIyN2UtZTFkYmZkNDQyNTAyXkEyXkFqcGdeQXVyODkzNTgxMDg@._V1_.jpg', 'title': 'Mortal Kombat', 'year': 2021, 'plot': "MMA fighter Cole Young seeks out Earth's greatest champions in order to stand against the enemies of Outworld in a high stakes battle for the universe."}, {'id': 'tt3554046', 'image': 'https://m.media-amazon.com/images/M/MV5BNjg3NmUwYjctMmIzYS00ZTNiLTlhNTYtMWMxNzE5YWIzNmQ4XkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_.jpg', 'title': 'Space Jam: A New Legacy', 'year': 2021, 'plot': 'NBA superstar LeBron James teams up with Bugs Bunny and the rest of the Looney Tunes for this long-awaited sequel.'}]
    # GETS TOP FIVE TV SHOWS
    # tv_data = top_tv_info()
    tv_data = [{'id': 'tt9208876', 'image': 'https://m.media-amazon.com/images/M/MV5BODNiODVmYjItM2MyMC00ZWQyLTgyMGYtNzJjMmVmZTY2OTJjXkEyXkFqcGdeQXVyNzk3NDUzNTc@._V1_.jpg', 'title': 'The Falcon and the Winter Soldier', 'year': 2021, 'plot': "Following the events of 'Avengers: Endgame,' Sam Wilson/Falcon and Bucky Barnes/Winter Soldier team up in a global adventure that tests their abilities -- and their patience."}, {'id': 'tt1520211', 'image': 'https://m.media-amazon.com/images/M/MV5BMTc5ZmM0OTQtNDY4MS00ZjMyLTgwYzgtOGY0Y2VlMWFmNDU0XkEyXkFqcGdeQXVyNDIzMzcwNjc@._V1_.jpg', 'title': 'The Walking Dead', 'year': 2010, 'plot': 'Sheriff Deputy Rick Grimes wakes up from a coma to learn the world is in ruins and must lead a group of survivors to stay alive.'}, {'id': 'tt7985576', 'image': 'https://m.media-amazon.com/images/M/MV5BY2U4ZTE1YTgtNmEzZi00N2E4LTk0MWItOTY3Y2RlNzliZTZjXkEyXkFqcGdeQXVyNjY1MTg4Mzc@._V1_.jpg', 'title': 'The Serpent', 'year': 2021, 'plot': "The twisting, real-life story of Charles Sobhraj, a murderer, thief and seductive master of disguise, who was a hidden darkness in the mid-70's on Asia's hippie trail."}, {'id': 'tt5774002', 'image': 'https://m.media-amazon.com/images/M/MV5BMDU4MWViOGItZGJjYi00YjczLTk1YmMtY2ZmNmY4YTllNDA0XkEyXkFqcGdeQXVyMTEyMjM2NDc2._V1_.jpg', 'title': "Jupiter's Legacy", 'year': 2021, 'plot': 'The first generation of superheroes has kept the world safe for nearly a century. Now their children must live up to their legacy in an epic drama that spans decades and navigates the dynamics of family, power and loyalty.'}, {'id': 'tt6741278', 'image': 'https://m.media-amazon.com/images/M/MV5BMmE1ODVhMGYtODYyYS00Mjc4LWIzN2EtYWZkZDg1MTUyNDkxXkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_.jpg', 'title': 'Invincible', 'year': 2021, 'plot': 'An adult animated series based on the Skybound/Image comic about a teenager whose father is the most powerful superhero on the planet.'}]
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
            return redirect(reverse("home"))
        return render(request, self.template_name, {
            "form": form,
            "header": "Signup"
        })


def search_details_view(request):
    # Gets the info collected from the api request
    movie_info = request.session.get('movie_info')
    item_plots = []
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
                # for index, item_id in enumerate(reply['d']):
                #     # GETS TV SHOW PLOTS
                #     url = "https://imdb8.p.rapidapi.com/title/get-plots"

                #     querystring = {"tconst": item_id['id']}

                #     headers = {
                #         'x-rapidapi-key': "1ddf0a8da3msh877010e622bf74dp10873cjsnd762a292965a",
                #         'x-rapidapi-host': "imdb8.p.rapidapi.com"
                #         }

                #     response = requests.request("GET", url, headers=headers, params=querystring)

                #     plot_reply = response.json()
                #     if 0 in plot_reply['plots']:
                #         plot = plot_reply['plots'][0]['text']
                #         print(index, plot)
                #     else:
                #         print(index, 'no')
                return redirect(reverse('search_details'))
            else:
                return redirect(reverse('actorspage'))
    # END HEADER SEARCH BAR
    search_form = SearchForm()
    return render(request, 'search_details.html', {
        'search_form': search_form,
        'movie_info': movie_info,
        'item_plots': item_plots
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
    # print(context)

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
    comments = Comment_model.objects.filter(movie_id=selection_id)
    print(comments)
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
        )
        context['search'] = SearchForm()
        return context


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
    return redirect(reverse('login'))


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
