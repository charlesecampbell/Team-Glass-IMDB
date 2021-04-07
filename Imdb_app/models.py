from django.db.models.fields.related import model
from Imdb_app.views import MoviesModelViewSet, TvshowsModelViewSet, MusicModelViewSet
from django.db import models


# Create your models here.

from django.contrib.auth.models import AbstractUser
# Create your models here.


class ApplicationUser(AbstractUser):
    display_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)

    REQUIRED_FIELDS = ['display_name']
    # Maybe have a favorite genre connected via FK or manytomany

# rename to Movie_Model


class Movie(models.Model):
    name = models.CharField(max_length=150)
    date_released = models.DateField()
    genre = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'
    # actors -- Maybe connect actors via a manytomany
    # Language, Budget,


class MovieReview(models.Model):
    review = models.TextField(max_length=250)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(ApplicationUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} {self.review} {self.movie}'


class Actor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    # possibly add link to their social media profile


# Genre Model connect with Movie and Music
