from django.db.models.enums import Choices
from django.db.models.fields.related import model
from Imdb_app.views import MoviesModelViewSet, TvshowsModelViewSet, MusicModelViewSet
from django.db import models
from modelchoices import Choices

# Create your models here.


class GenresModel(models.Model):
    MOVIES = 'Movies_Genres'
    TVSHOWS = 'Tvshows_Genres'
    MUSIC = 'Music_Genres'
    FAVORITES = 'Favorites_Genres'
    CHOICES = (
        (MOVIES, 'New_Movies', 'Dramas', 'Actions', 'SciFi', 'Horrors'),
        (TVSHOWS, 'New_Tvshows', 'Games', 'Cartoons', 'Teens', 'Cooking'),
        (MUSIC, 'New_Music', 'Rap', 'Country', 'Latin', 'Blues', 'Rock'),
    )

    def save(self, *args, **kwargs):
        self.favorites = self.Movies + self.TvShows + self.Music
        super(GenresModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.favorites
