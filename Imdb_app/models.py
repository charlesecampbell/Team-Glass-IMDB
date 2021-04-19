from django.contrib.auth.models import AbstractUser
# from django_mysql.models import ListCharField
from django.utils import timezone
from django.db import models
# Create your models here.


class ApplicationUser(AbstractUser):
    display_name = models.CharField(max_length=50)
    bio = models.CharField(blank=True, max_length=200, null=True)
    user_image = models.FileField(blank=True, null=True, upload_to='images/')

    def __str__(self):
        return f'{self.display_name}'


class Comment_model(models.Model):
    input_field = models.TextField()
    movie_image = models.URLField(max_length=500)
    movie_title = models.CharField(max_length=180)
    commenter = models.ForeignKey(ApplicationUser, on_delete=models.CASCADE)
    movie_id = models.CharField(max_length=25)
    date_created = models.DateTimeField(default=timezone.now)
    recommended = models.BooleanField(null=True)


# Model for Liked Moviespy
class LikedMoviesModel(models.Model):
    movie_title = models.CharField(max_length=250)
    movie_img = models.URLField(max_length=500)
    movie_release = models.CharField(max_length=20)
    movie_actors = models.CharField(max_length=500)
    movie_id = models.CharField(max_length=25)
    user = models.ForeignKey(ApplicationUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} likes {self.movie_title}'


# Model for Want To See
class WantToSeeModel(models.Model):
    movie_title = models.CharField(max_length=250)
    movie_img = models.URLField(max_length=500)
    movie_release = models.CharField(max_length=20)
    movie_actors = models.CharField(max_length=500)
    movie_id = models.CharField(max_length=25)
    user = models.ForeignKey(ApplicationUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} wants to see {self.movie_title}'


# Model for Have Seen
class HaveSeenModel(models.Model):
    movie_title = models.CharField(max_length=250)
    movie_img = models.URLField(max_length=500)
    movie_release = models.CharField(max_length=20)
    movie_actors = models.CharField(max_length=500)
    movie_id = models.CharField(max_length=25)
    user = models.ForeignKey(ApplicationUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} Has Seen {self.movie_title}'
