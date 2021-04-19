import requests
from decouple import config
from Imdb_app.models import HaveSeenModel, WantToSeeModel


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


def run_search(request, search_form):
    if search_form.is_valid():
        data = search_form.cleaned_data
        reply = search_bar(data['search_actors_or_movies'])
        page_decision = reply['d'][0]['id'][:2]
        movie_info = results_data(reply)
        request.session['movie_info'] = movie_info
        if page_decision != 'nm':
            for index, item_id in enumerate(movie_info):
                # GETS TV SHOW PLOTS
                if item_id['id'][0:2] != 'nm':
                    url = "https://imdb8.p.rapidapi.com/title/get-plots"

                    querystring = {"tconst": item_id['id']}

                    headers = {
                        'x-rapidapi-key': config('MAIN_IMDB_KEY'),
                        'x-rapidapi-host': "imdb8.p.rapidapi.com"
                        }

                    response = requests.request(
                        "GET",
                        url,
                        headers=headers,
                        params=querystring)

                    plot_reply = response.json()
                    if plot_reply['plots']:
                        movie_info[index]['plot'] =\
                            plot_reply['plots'][0]['text']
                    else:
                        movie_info[index]['plot'] = 'No Plot Available'
                else:
                    movie_info[index]['plot'] = 'No Plot Available'

                if request.user.id is not None:
                    seen = HaveSeenModel.objects.filter(
                        movie_id=item_id['id'],
                        user=request.user
                        )

                    if seen:
                        movie_info[index]['seen'] = True
                    else:
                        movie_info[index]['seen'] = False

                if request.user.id is not None:
                    want = WantToSeeModel.objects.filter(
                        movie_id=item_id['id'],
                        user=request.user
                        )
                    if want:
                        movie_info[index]['want'] = True
                    else:
                        movie_info[index]['want'] = False
            print(movie_info)
        return(movie_info, page_decision)


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

        # GETS MOVIE PLOTS
        url = "https://imdb8.p.rapidapi.com/title/get-plots"

        querystring = {"tconst": movie}

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

        plot_reply = response.json()
        plot = plot_reply['plots'][0]['text']
        home_page_movie_data.append(
            {
                "id": top_reply['title']['id'][7:-1],
                "image": top_reply['title']['image']['url'],
                "title": top_reply['title']['title'],
                "year": top_reply['title']['year'],
                'plot': plot
            })
    print(home_page_movie_data)
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

        # GETS TV SHOW PLOTS
        url = "https://imdb8.p.rapidapi.com/title/get-plots"

        querystring = {"tconst": show_id}

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

        plot_reply = response.json()
        plot = plot_reply['plots'][0]['text']

        home_page_tv_data.append(
            {
                "id": tv_reply['title']['id'][7:-1],
                "image": tv_reply['title']['image']['url'],
                "title": tv_reply['title']['title'],
                "year": tv_reply['title']['year'],
                'plot': plot
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
