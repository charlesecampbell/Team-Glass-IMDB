# Generated by Django 3.1.7 on 2021-04-20 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Imdb_app', '0002_auto_20210419_1750'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment_model',
            name='user_image',
            field=models.URLField(max_length=500, null=True),
        ),
    ]
