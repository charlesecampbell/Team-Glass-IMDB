# Generated by Django 3.1.7 on 2021-04-20 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Imdb_app', '0003_comment_model_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment_model',
            name='user_image',
            field=models.TextField(max_length=500, null=True),
        ),
    ]
