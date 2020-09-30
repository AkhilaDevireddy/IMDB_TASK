from django.db import models
from django_mysql.models import ListTextField


class IMDB(models.Model):
    name_director = models.CharField(primary_key=True, default='0000000', max_length=100)
    name = models.CharField(max_length=100)
    director = models.CharField(max_length=50)
    imdb_score = models.FloatField()
    popularity_99 = models.FloatField()
    genre = ListTextField(base_field=models.CharField(max_length=25), size=50)  # Maximum of 50 ids in list
