from .models import IMDB
from rest_framework import serializers


class IMDBSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = IMDB
        fields = ('name_director', 'name', 'director', 'imdb_score', 'popularity_99', 'genre')
