import requests
from decouple import config
from Imdb_app.forms import SearchForm
from django.shortcuts import redirect, reverse


def search_bar(query):
    # Api Call With the Search Results
    url = "https://imdb8.p.rapidapi.com/auto-complete"
    querystring = {"q": query}

    headers = {
        'x-rapidapi-key': config('MAIN_IMDB_KEY'),
        'x-rapidapi-host': "imdb8.p.rapidapi.com"
        }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)

    reply = response.json()
    return reply


def search_bar_request(request):
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


def results_data(reply):
    movie_info = []
    for poster in reply['d']:
        if 'y' in poster and 'i' in poster:
            movie_info.append(
                {
                    'poster': poster['i']['imageUrl'],
                    'id': poster['id'],
                    'year': poster['y'],
                    'title': poster['l']
                })
        elif 'i' not in poster and 'y' not in poster:
            movie_info.append(
                {
                    'poster': 'NO POSTER AVAILABLE',
                    'id': poster['id'],
                    'year': 'NO YEAR AVAILABLE',
                    'title': poster['l']
                })
        elif 'y' not in poster:
            movie_info.append(
                {
                    'poster': poster['i']['imageUrl'],
                    'id': poster['id'],
                    'year': 'NO YEAR AVAILABLE',
                    'title': poster['l']
                })
        elif 'i' not in poster:
            movie_info.append(
                {
                    'id': poster['id'],
                    'year': poster['y'],
                    'title': poster['l']
                })
    return (movie_info)


def top_movies_id():
    # GET A TOP FIVE MOVIE LIST TITLE ID'S
    url = "https://imdb8.p.rapidapi.com/title/get-most-popular-movies"

    querystring = {
        "homeCountry": "US",
        "purchaseCountry": "US",
        "currentCountry": "US"
        }

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

    reply = response.json()
    top_five_list = []
    count = 0
    for title_id in reply:
        if count < 5:
            top_five_list.append(title_id[7:-1])
            count += 1
    return top_five_list


def top_movie_data():
    movie_data = top_movies_id()
    # USE TITLE ID'S TO GET MOVIE INFO
    home_page_movie_data = []
    for movie in movie_data:
        url = "https://imdb8.p.rapidapi.com/title/get-top-stripe"

        querystring = {
            "tconst": movie,
            "currentCountry": "US",
            "purchaseCountry": "US"
            }

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

        top_reply = response.json()
        home_page_movie_data.append(
            {
                "id": top_reply['title']['id'][7:-1],
                "image": top_reply['title']['image']['url'],
                "title": top_reply['title']['title'],
                "year": top_reply['title']['year']
            })
    return home_page_movie_data


def top_tv_ids():
    # GET TOP 5 TV IDS
    url = "https://imdb8.p.rapidapi.com/title/get-most-popular-tv-shows"

    querystring = {
        "homeCountry": "US",
        "purchaseCountry": "US",
        "currentCountry": "US"
        }

    headers = {
        'x-rapidapi-key': config('MAIN_IMDB_KEY'),
        'x-rapidapi-host': "imdb8.p.rapidapi.com"
        }

    response = requests.request(
        "GET",
        url, headers=headers,
        params=querystring
        )

    reply = response.json()
    top_tv_ids = []
    count2 = 0
    for id in reply:
        if count2 < 5:
            top_tv_ids.append(id[7:-1])
            count2 += 1
    return top_tv_ids


def top_tv_info():
    # REQUEST TO GET THE TOP 5 TV INFO
    tv_data = top_tv_ids()
    home_page_tv_data = []
    for show_id in tv_data:
        url = "https://imdb8.p.rapidapi.com/title/get-top-stripe"

        querystring = {
            "tconst": show_id,
            "currentCountry": "US",
            "purchaseCountry": "US"
            }

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

        tv_reply = response.json()
        home_page_tv_data.append(
            {
                "id": tv_reply['title']['id'][7:-1],
                "image": tv_reply['title']['image']['url'],
                "title": tv_reply['title']['title'],
                "year": tv_reply['title']['year']
            })
    print(home_page_tv_data)
    return home_page_tv_data


def hollywood_news():
    # GETS HOLLYWOOD NEWS
    url = "https://imdb8.p.rapidapi.com/title/get-news"

    querystring = {"tconst": "tt13429362", "limit": "25"}

    headers = {
        'x-rapidapi-key': "1ddf0a8da3msh877010e622bf74dp10873cjsnd762a292965a",
        'x-rapidapi-host': "imdb8.p.rapidapi.com"
        }

    response = requests.request(
        "GET",
        url,
        headers=headers,
        params=querystring
        )

    reply = response.json()
    return reply['items']
