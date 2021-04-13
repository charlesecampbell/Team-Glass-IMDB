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

    # GET A TOP FIVE MOVIE LIST TITLE ID'S
    # url = "https://imdb8.p.rapidapi.com/title/get-most-popular-movies"

    # querystring = {
    #     "homeCountry": "US",
    #     "purchaseCountry": "US",
    #     "currentCountry": "US"
    #     }

    # headers = {
    #     'x-rapidapi-key': "1ddf0a8da3msh877010e622bf74dp10873cjsnd762a292965a",
    #     'x-rapidapi-host': "imdb8.p.rapidapi.com"
    #     }

    # response = requests.request(
    #     "GET",
    #     url,
    #     headers=headers,
    #     params=querystring
    #     )

    # reply = response.json()
    # top_five_list = []
    # count = 0
    # for title_id in reply:
    #     if count < 5:
    #         top_five_list.append(title_id[7:-1])
    #         count += 1

    # USE TITLE ID'S TO GET MOVIE INFO
    home_page_movie_data = [{'id': 'tt5034838', 'image': 'https://m.media-amazon.com/images/M/MV5BZmYzMzU4NjctNDI0Mi00MGExLWI3ZDQtYzQzYThmYzc2ZmNjXkEyXkFqcGdeQXVyMTEyMjM2NDc2._V1_.jpg', 'title': 'Godzilla vs. Kong', 'year': 2021}, {'id': 'tt3480822', 'image': 'https://m.media-amazon.com/images/M/MV5BYjdmODAzNTctNWU1NS00ZmRiLWFiM2YtMjAyNzgzZWJlZjhlXkEyXkFqcGdeQXVyMTEyMjM2NDc2._V1_.jpg', 'title': 'Black Widow', 'year': 2021}, {'id': 'tt12361974', 'image': 'https://m.media-amazon.com/images/M/MV5BYjI3NDg0ZTEtMDEwYS00YWMyLThjYjktMTNlM2NmYjc1OGRiXkEyXkFqcGdeQXVyMTEyMjM2NDc2._V1_.jpg', 'title': "Zack Snyder's Justice League", 'year': 2021}, {'id': 'tt0293429', 'image': 'https://m.media-amazon.com/images/M/MV5BY2ZlNWIxODMtN2YwZi00ZjNmLWIyN2UtZTFkYmZkNDQyNTAyXkEyXkFqcGdeQXVyODkzNTgxMDg@._V1_.jpg', 'title': 'Mortal Kombat', 'year': 2021}, {'id': 'tt3554046', 'image': 'https://m.media-amazon.com/images/M/MV5BNjg3NmUwYjctMmIzYS00ZTNiLTlhNTYtMWMxNzE5YWIzNmQ4XkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_.jpg', 'title': 'Space Jam: A New Legacy', 'year': 2021}]
    # for movie in top_five_list:
    #     url = "https://imdb8.p.rapidapi.com/title/get-top-stripe"

    #     querystring = {
    #         "tconst": movie,
    #         "currentCountry": "US",
    #         "purchaseCountry": "US"
    #         }

    #     headers = {
    #         'x-rapidapi-key': "1ddf0a8da3msh877010e622bf74dp10873cjsnd762a292965a",
    #         'x-rapidapi-host': "imdb8.p.rapidapi.com"
    #     }

    #     response = requests.request(
    #         "GET",
    #         url,
    #         headers=headers,
    #         params=querystring
    #         )

    #     top_reply = response.json()
    #     home_page_movie_data.append(
    #         {
    #             "id": top_reply['title']['id'][7:-1],
    #             "image": top_reply['title']['image']['url'],
    #             "title": top_reply['title']['title'],
    #             "year": top_reply['title']['year']
    #         })
    # print(home_page_movie_data)

    # GET TOP 5 TV IDS
    # url = "https://imdb8.p.rapidapi.com/title/get-most-popular-tv-shows"

    # querystring = {"homeCountry": "US", "purchaseCountry": "US", "currentCountry": "US"}

    # headers = {
    #     'x-rapidapi-key': "1ddf0a8da3msh877010e622bf74dp10873cjsnd762a292965a",
    #     'x-rapidapi-host': "imdb8.p.rapidapi.com"
    #     }

    # response = requests.request(
    #     "GET",
    #     url, headers=headers,
    #     params=querystring
    #     )

    # reply = response.json()
    # top_tv_ids = []
    # count2 = 0
    # for id in reply:
    #     if count2 < 5:
    #         top_tv_ids.append(id[7:-1])
    #         count2 += 1
    # print(top_tv_ids)

    # REQUEST TO GET THE TOP 5 TV INFO
    home_page_tv_data = [{'id': 'tt9208876', 'image': 'https://m.media-amazon.com/images/M/MV5BODNiODVmYjItM2MyMC00ZWQyLTgyMGYtNzJjMmVmZTY2OTJjXkEyXkFqcGdeQXVyNzk3NDUzNTc@._V1_.jpg', 'title': 'The Falcon and the Winter Soldier', 'year': 2021}, {'id': 'tt1520211', 'image': 'https://m.media-amazon.com/images/M/MV5BMTc5ZmM0OTQtNDY4MS00ZjMyLTgwYzgtOGY0Y2VlMWFmNDU0XkEyXkFqcGdeQXVyNDIzMzcwNjc@._V1_.jpg', 'title': 'The Walking Dead', 'year': 2010}, {'id': 'tt7985576', 'image': 'https://m.media-amazon.com/images/M/MV5BY2U4ZTE1YTgtNmEzZi00N2E4LTk0MWItOTY3Y2RlNzliZTZjXkEyXkFqcGdeQXVyNjY1MTg4Mzc@._V1_.jpg', 'title': 'The Serpent', 'year': 2021}, {'id': 'tt5774002', 'image': 'https://m.media-amazon.com/images/M/MV5BMDU4MWViOGItZGJjYi00YjczLTk1YmMtY2ZmNmY4YTllNDA0XkEyXkFqcGdeQXVyMTEyMjM2NDc2._V1_.jpg', 'title': "Jupiter's Legacy", 'year': 2021}, {'id': 'tt6741278', 'image': 'https://m.media-amazon.com/images/M/MV5BMmE1ODVhMGYtODYyYS00Mjc4LWIzN2EtYWZkZDg1MTUyNDkxXkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_.jpg', 'title': 'Invincible', 'year': 2021}]
    # for show_id in top_tv_ids:
    #     url = "https://imdb8.p.rapidapi.com/title/get-top-stripe"

    #     querystring = {
    #         "tconst": show_id,
    #         "currentCountry": "US",
    #         "purchaseCountry": "US"
    #         }

    #     headers = {
    #         'x-rapidapi-key': "1ddf0a8da3msh877010e622bf74dp10873cjsnd762a292965a",
    #         'x-rapidapi-host': "imdb8.p.rapidapi.com"
    #         }

    #     response = requests.request(
    #         "GET",
    #         url,
    #         headers=headers,
    #         params=querystring
    #         )

    #     tv_reply = response.json()
    #     home_page_tv_data.append(
    #         {
    #             "id": tv_reply['title']['id'][7:-1],
    #             "image": tv_reply['title']['image']['url'],
    #             "title": tv_reply['title']['title'],
    #             "year": tv_reply['title']['year']
    #         })

    search_form = SearchForm()
    context.update({
        'search_form': search_form,
        'user': user,
        'home_page_movie_data': home_page_movie_data,
        'homepage_tv_data': home_page_tv_data
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
