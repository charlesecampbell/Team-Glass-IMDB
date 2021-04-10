import requests


def search_bar(query):
    # Api Call With the Search Results
    url = "https://imdb8.p.rapidapi.com/auto-complete"
    querystring = {"q": query}

    headers = {
        'x-rapidapi-key': "1ddf0a8da3msh877010e622bf74dp10873cjsnd762a292965a",
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
