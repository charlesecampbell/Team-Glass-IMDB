from django.contrib.auth.models import AbstractUser
from django_mysql.models import ListCharField
from django.utils import timezone
# Create your models here.


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


class Comment_model(models.Model):
    input_field = models.TextField()
    movie = models.URLField(max_length=500),
    commenter = models.ForeignKey(ApplicationUser, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)
    recommended = models.BooleanField(null=True)
