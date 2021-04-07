from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from imdb_app.models import UsersModel, MoviesModel, ActorsModel, MusicModel, TvshowsModel, GenreModel
from rest_framework.decorators import action
from rest_framework.response import Response


# Create your views here.
class UsersModelViewSet(ModelViewSet):
    @action(detail=False)
    def Favorites(self, request):
        favorites = Users.objects.filter(favorites=True).order_by(
            'watched_date').reverse()

    @action(detail=False)
    def Watched(self, request):
        watched = UsersModel.objects.filter(watched=False).order_by(
            'watched_date').reverse()


class MoviesModelViewSet(ModelViewSet):
    @action(detail=True, methods=['movies'])
    def ThumbsUp1(self, request, pk=None):
        movies = self.get_object()
        movies.thumbsup1 += 1
        movies.save()
        return Response({'status': 'ThumsUp1'})

    @action(detail=True, methods=['movies'])
    def ThumbsUp2(self, request, pk=None):
        movies = self.get_object()
        movies.thumbsup2 += 1
        movies.save()
        return Response({'status': 'ThumsUp2'})

    @action(detail=True, methods=['movies'])
    def ThumbsUp3(self, request, pk=None):
        movies = self.get_object()
        movies.thumbsup3 += 1
        movies.save()
        return Response({'status': 'ThumsUp3'})

    @action(detail=True, methods=['movies'])
    def ThumbsDown1(self, request, pk=None):
        movies = self.get_object()
        movies.thumbsdown1 += 1
        movies.save()
        return Response({'status': 'ThumsDown1'})

    @action(detail=True, methods=['movies'])
    def ThumbsDown2(self, request, pk=None):
        movies = self.get_object()
        movies.thumbsdown2 += 1
        movies.save()
        return Response({'status': 'ThumsDown2'})

    @action(detail=True, methods=['movies'])
    def ThumbsDown3(self, request, pk=None):
        movies = self.get_object()
        movies.thumbsdown3 += 1
        movies.save()
        return Response({'status': 'ThumsDown3'})


class ActorsModelViewSet(ModelViewSet):


class MusicModelViewSet(ModelViewSet):


class TvshowsModelViewSet(ModelViewSet):


class GenreModelViewSet(ModelViewSet):
