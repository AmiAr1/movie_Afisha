from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Director(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=255, null=True)
    duration = models.IntegerField(default=0)
    director = models.ForeignKey(Director, on_delete=models.CASCADE,
                                 null=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    text = models.TextField(max_length=255)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE,
                              null=True)
    stars = models.SmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)],
        default=1)

    def rating_average(self):
        reviews = Review.objects.filter(movie=self.movie)
        if not reviews.exists():
            return 0
        sum_star = sum(i.stars for i in reviews)
        return round(sum_star / reviews.count(), 1)

    def __str__(self):
        return self.text

