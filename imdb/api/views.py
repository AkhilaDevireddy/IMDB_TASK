from django.db.models import Q
from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from .models import IMDB
from rest_framework import viewsets
from .serializers import IMDBSerializer
from rest_framework.views import APIView, Response
from rest_framework.decorators import api_view


# class IMDBViewSet(viewsets.ModelViewSet):
#     queryset = IMDB.objects.all()
#     serializer_class = IMDBSerializer


# class CustomView(APIView):
#     # @api_view(['GET'])
#     # def get(self, request, format=None):
#     #     return Response("Some Get Response")

#     # @api_view(['GET', 'POST', 'DELETE'])
#     # def post(self, request, format=None):
#     #     return Response("Some Post Response")
#     pass

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
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
            print("IMDB_SCORE")
            print(imdb_score_pointer)
            imdb_movies = imdb_movies.filter(imdb_score__gte=imdb_score_pointer)

        # elif genre_type:
        #     print("GENRE_TYPE")
        #     print(genre_type)
        #     imdb_movies = imdb_movies.filter(genre__contains=genre_type)
        
        imdb_serializer = IMDBSerializer(imdb_movies, many=True)
        return JsonResponse(imdb_serializer.data, safe=False)
        # 'safe=False' for objects serialization
 
    elif request.method == 'POST':
        imdb_data = JSONParser().parse(request)
        # imdb_serializer = IMDBSerializer(data=imdb_data)
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
            # return JsonResponse(imdb, status='201')
        except Exception as exc:
            print(exc)
            return JsonResponse("exc", status='400')
            # imdb_serializer.is_valid()
            # return JsonResponse(imdb_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # if imdb_serializer.is_valid():
        #     imdb_serializer.save()
        #     print("VALID")
        #     return JsonResponse(imdb_serializer.data, status=status.HTTP_201_CREATED) 
        # print("INVALID")
        # return JsonResponse(imdb_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # elif request.method == 'PUT':
    #     imdb_data = JSONParser().parse(request)
    #     # imdb_serializer = IMDBSerializer(data=imdb_data)
    #     name_director = request.query_params.get('name_director', None)
    #     imdb_movies = imdb_movies.filter(Q(name_director__icontains=name_director))
    #     for key in imdb_data.keys():
    #         if key == 'name':
    #             imdb_movies.update(name=imdb_data[key])
    #         elif key == 'director':
    #             imdb_movies.update(director=imdb_data[key])
    #         elif key == 'genre':
    #             imdb_movies.update(genre=imdb_data[key])
    #         elif key == 'imdb_score':
    #             imdb_movies.update(imdb_score=imdb_data[key])
    #         elif key == '99popularity':
    #             imdb_movies.update(popularity_99=imdb_data[key])

    #         imdb_movies = imdb_movies.filter(Q(name_director__icontains=name_director))
    #         imdb_serializer = IMDBSerializer(imdb_movies, many=True)
    #         return JsonResponse(imdb_movies, status='201')

    elif request.method == 'DELETE':
        name_director = request.query_params.get('name_director', None)
        imdb_movies = imdb_movies.filter(Q(name_director__icontains=name_director))
        count = imdb_movies.delete()
        return JsonResponse({'message': '{} IMDB Record deleted successfully!'.format(count[0])}, status='201')
