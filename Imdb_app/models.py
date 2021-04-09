from django.db import models
from django.contrib.auth.models import AbstractUser
from django_mysql.models import ListCharField
from django.utils import timezone
# Create your models here.

# user model
class ApplicationUser(AbstractUser):
    display_name = models.CharField(max_length=50)
    likes = ListCharField(
        base_field=models.URLField(max_length=500),
        max_length=5000
    )
    want_to_see = ListCharField(
        base_field=models.URLField(max_length=500), 
        max_length=5000
    )
    have_seen = ListCharField(
        base_field=models.URLField(max_length=500),
        max_length=5000, 
    )
    # fav_genres = models.ManyToManyField(Genre)
    # email = models.EmailField(max_length=50)
    
    REQUIRED_FIELDS = ['display_name']


class Comment_model(models.Model):
    input_field = models.TextField()
    movie = models.URLField(max_length=500)
    commenter = models.ForeignKey(ApplicationUser, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)
    recommended = models.BooleanField(null=True)



    # can go with being a simple foreignKey or having a list via manytomany
# Genre Model connect with Movie and Music