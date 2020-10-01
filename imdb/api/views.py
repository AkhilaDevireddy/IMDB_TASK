from django.db.models import Q
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view

from .models import IMDB
from .serializers import IMDBSerializer


@api_view(['GET', 'POST', 'DELETE'])
def imdb_list(request):
    print(request.method)
    imdb_movies = IMDB.objects.all()
    if request.method == 'GET':

        movie_name = request.query_params.get('name', None)
        imdb_score_pointer = request.query_params.get('imdb_score', None)
        genre_type = request.query_params.get('genre', None)
        if movie_name is not None:
            print("MOVIE_NAME")
            print(movie_name)
            imdb_movies = imdb_movies.filter(name__icontains=movie_name)

        elif imdb_score_pointer is not None:
            imdb_movies = imdb_movies.filter(imdb_score__gte=imdb_score_pointer)

        # elif genre_type:
        #     print("GENRE_TYPE")
        #     print(genre_type)
        #     imdb_movies = imdb_movies.filter(genre__contains=genre_type)
        
        imdb_serializer = IMDBSerializer(imdb_movies, many=True)
        return JsonResponse(imdb_serializer.data, safe=False)
 
    elif request.method == 'POST':
        imdb_data = JSONParser().parse(request)
        try:
            new_imdb_account = IMDB(
                                    name_director=imdb_data['name'] + imdb_data['director'],
                                    name=imdb_data['name'],
                                    director=imdb_data['director'],
                                    imdb_score=imdb_data['imdb_score'],
                                    popularity_99=imdb_data['99popularity'],
                                    genre=imdb_data['genre']
                                )
            new_imdb_account.save()
            imdb_movies = imdb_movies.filter(name_director__icontains=imdb_data['name'] + imdb_data['director'])
            imdb_serializer = IMDBSerializer(imdb_movies, many=True)
            return JsonResponse(imdb_serializer.data, safe=False)
        except Exception as exc:
            print(exc)
            return JsonResponse("exc", status='400')

    elif request.method == 'DELETE':
        name_director = request.query_params.get('name_director', None)
        imdb_movies = imdb_movies.filter(Q(name_director__icontains=name_director))
        count = imdb_movies.delete()
        return JsonResponse({'message': '{} IMDB Record deleted successfully!'.format(count[0])}, status='201')
