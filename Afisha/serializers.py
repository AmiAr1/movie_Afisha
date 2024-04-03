from rest_framework import serializers
from Afisha.models import *


# class DirectorSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Director
#         fields = '__all__'
#
#
# class ReviewSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Review
#         fields = '__all__'
#
#
# class MovieSerializers(serializers.ModelSerializer):
#     director = DirectorSerializers()
#     reviews = ReviewSerializers(many=True)
#
#     class Meta:
#         model = Movie
#         fields = 'id director title duration reviews'.split()


# from rest_framework import serializers
# from .models import Director, Movie, Review
#

class DirectorListSerializer(serializers.ModelSerializer):
    movies_count = serializers.SerializerMethodField()

    class Meta:
        model = Director
        fields = 'id name movies_count'.split()

    def get_movies_count(self, director):
        return director.movie_set.all().count()


class MovieListSerializer(serializers.ModelSerializer):
    director_name = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = 'id title description duration director_name'.split()

    def get_director_name(self, movie):
        if movie.director:
            return movie.director.name
        return None


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id text movie'.split()


class MovieRatingSerializer(serializers.ModelSerializer):
    name_movie = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = 'id stars name_movie rating_average'.split()

    def get_name_movie(self, movies):
        return movies.movie.title


class DirectorValidationSerializer(serializers.Serializer):
    name = serializers.RegexField(regex=r'^[a-zA-Zа-яА-Я ]*$', max_length=255,
                                  error_messages={'invalid': "Name should contain only letters"})

    def get_movie_name(self, director):
        if director.movie:
            return director.movie.title
        return None


class ReviewValidationSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=255)
    stars = serializers.IntegerField(min_value=1, max_value=5)
    movie = serializers.CharField(max_length=255)


class MovieValidateSerializer(serializers.Serializer):
    title = serializers.RegexField(regex=r'^[a-zA-Zа-яА-Я ]*$', max_length=255,
                                   error_messages={'invalid': "Name should contain only letters"})
    description = serializers.CharField(min_length=1, max_length=255)
    duration = serializers.IntegerField(min_value=0)
    director = serializers.CharField(max_length=255)


