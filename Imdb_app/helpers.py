import requests


def check_model(user, model, id):
    info = model.objects.filter(user=user, movie_id=id).first()
    if info is None:
        return None
    else:
        return info.movie_id


def check_model_x_api(movie_id, obj, str):
    if movie_id is None:
        obj[str] = 'no'
        return
    else:
        api_id = obj['d'][0]['id']
        if movie_id == api_id:
            obj[str] = 'yes'


def retrieve_movie_trailer(id):
    # GETS THE TRAILER LINK WITH THE MOVIE ID
    url = "https://imdb8.p.rapidapi.com/title/get-video-playback"

    querystring = {"viconst": id, "region": "US"}

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

    reply2 = response.json()
    trailer_link = reply2['resource']['encodings'][1]['playUrl']
    encode_type = reply2['resource']['encodings'][1]['mimeType']
    return(trailer_link, encode_type)


def retrieve_movie_trailer_id(id):
    # GETS THE TRAILER ID WITH THE MOVIE ID
    url = "https://imdb8.p.rapidapi.com/title/get-videos"

    querystring = {"tconst": id, "limit": "25", "region": "US"}

    headers = {
        'x-rapidapi-key': "1ddf0a8da3msh877010e622bf74dp10873cjsnd762a292965a",
        'x-rapidapi-host': "imdb8.p.rapidapi.com"
        }

    response = requests.request(
        "GET",
        url,
        headers=headers,
        params=querystring)

    reply = response.json()
    get_vid_id = reply['resource']['videos'][0]['id'][9:]
    return retrieve_movie_trailer(get_vid_id)