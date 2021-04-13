def check_model(user,model, id):
    info = model.objects.filter(user=user, movie_id=id).first()
    if info == None:
        return None
    else:
        return info.movie_id


def check_model_x_api(movie_id, obj, str):
    if movie_id == None:
        obj[str] = 'no'
        return
    else:
        api_id = obj['d'][0]['id']
        if movie_id == api_id:
            obj[str] = 'yes'
            