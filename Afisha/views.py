from rest_framework.decorators import api_view
from rest_framework.response import Response
from Afisha.serializers import *
from .models import Movie
# Create your views here.


@api_view(["GET", 'POST'])
def movies_view(request):
    if request.method == 'GET':
        products = Movie.objects.all()
        data = MovieListSerializer(products, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        # 0 шаг проверка данных validation
        serializers = MovieValidateSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        # 1 шаг получаем данные из тела запроса
        title = serializers.validated_data.get('title')
        description = serializers.validated_data.get('description')
        duration = serializers.validated_data.get('duration')
        director_name = serializers.validated_data.get('director')
        # Проверяем, существует ли режиссер с указанным именем
        director, _ = Director.objects.get_or_create(name=director_name)
        if Movie.objects.filter(title=title).exists():
            return Response({"error": "Movie with this name already exists"}, status=404)
        #  2 шаг создаем обьект использую данные
        movie = Movie.objects.create(
            title=title, description=description,
            duration=duration, director=director
        )
        #  3 шаг возвращаем созданный обьект

        return Response(data=MovieListSerializer(movie).data)


@api_view(['GET', 'POST'])
def review_view(request):
    if request.method == 'GET':
        products = Review.objects.all()
        data = ReviewListSerializer(products, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        # 0 шаг проверка данных validation
        serializers = ReviewValidationSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        # 1 шаг получаем данные из тела запроса
        text = serializers.validated_data.get('text')
        stars = serializers.validated_data.get('stars')
        movie = serializers.validated_data.get('movie')
        # найти фильм по его названию
        try:
            movie = Movie.objects.get(title=movie)
        except Movie.DoesNotExist:
            return Response({'error': "Movie does not exist"}, status=404)

        if Review.objects.filter(text=text).exists():
            return Response({'error': "Review with this allready exists"}, status=400)

        #  2 шаг создаем обьект использую данные
        review = Review.objects.create(
            text=text, stars=stars, movie=movie
        )
        #  3 шаг возвращаем созданный обьект
        return Response(data=ReviewValidationSerializer(review).data)


@api_view(['GET', 'POST'])
def director_view(request):
    if request.method == 'GET':
        products = Director.objects.all()
        data = DirectorListSerializer(products, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        # 0 шаг проверка данных validation
        serializers = DirectorValidationSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        # 1 шаг получаем данные из тела запроса
        name = serializers.validated_data.get('name')
        if Director.objects.filter(name=name).exists():
            return Response({"error": "Director with this name already exists"}, status=404)
        #  2 шаг создаем обьект использую данные
        director = Director.objects.create(
            name=name,
        )
        #  3 шаг возвращаем созданный обьект

        return Response(data=DirectorValidationSerializer(director).data)


@api_view(['GET'])
def movie_review(request):
        product = Review.objects.all()
        data = MovieRatingSerializer(product, many=True).data
        return Response(data=data)


@api_view(['GET', 'PUT', 'DELETE'])
def detail_movie(request, id_movie):
    try:
        movie = Movie.objects.get(id=id_movie)
    except Movie.DoesNotExist:
        return Response({'message': "такого фильма не существует"}, status=404)

    if request.method == 'GET':
        data = MovieListSerializer(instance=movie).data
        return Response(data=data)

    elif request.method == 'PUT':
        serializer = MovieValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        movie.title = serializer.validated_data.get('title')
        movie.description = serializer.validated_data.get('description')
        movie.duration = serializer.validated_data.get('duration')
        director_name = serializer.validated_data.get('director')
        director, _ = Director.objects.get_or_create(name=director_name)
        movie.director = director
        movie.save()
        return Response(data=MovieValidateSerializer(movie).data)
    else:
        movie.delete()
        return Response(status=204)


@api_view(['GET', 'PUT', 'DELETE'])
def detail_director(request, id_director):
    try:
        director = Director.objects.get(id=id_director)
    except Director.DoesNotExist:
        return Response({'message': "такого режиссера не существует"}, status=404)

    if request.method == 'GET':
        data = DirectorListSerializer(director).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializers = DirectorValidationSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        director.name = serializers.validated_data.get('name')
        director.save()
        return Response(data=DirectorValidationSerializer(director).data)
    else:
        director.delete()
        return Response(status=204)


@api_view(['GET', 'PUT', 'DELETE'])
def detail_review(request, id_review):
    try:
        review = Review.objects.get(id=id_review)
    except Review.DoesNotExist:
        return Response({'message': "такого режиссера не существует"}, status=404)
    if request.method == 'GET':
        serializer = ReviewListSerializer(review)
        return Response(data=serializer.data)
    elif request.method == 'PUT':
        serializers = ReviewValidationSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        review.text = serializers.validated_data.get('text')
        review.save()
        return Response(data=ReviewValidationSerializer(review).data)
    else:
        review.delete()
        return Response(status=204)











