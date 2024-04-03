from .views import *
from django.urls import path


urlpatterns = [
    path('movie/', movies_view),  # пост гет
    path('movie/<int:id_movie>/', detail_movie),  # put get delete

    path('review/', review_view),  # get пост
    path('review/<int:id_review>/', detail_review),  # пут делете пост get

    path('directors/', director_view),  # get post
    path('directors/<int:id_director>/', detail_director),  # gey delete put

    path('movie/review/', movie_review),
]