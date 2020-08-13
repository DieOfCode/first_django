from datetime import date

from django.db import models


# Create your models here.
from django.urls import reverse


class Category(models.Model):
    name = models.CharField("Category", max_length=150)
    description = models.TextField("Description")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Actor(models.Model):
    name = models.CharField("Name", max_length=100)
    age = models.PositiveSmallIntegerField("Age", default=0)
    description = models.TextField("Description")
    image = models.ImageField("Picture", upload_to="actors/")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("actor_detail", kwargs={"slug":self.name})

    class Meta:
        verbose_name = "Actors and Compositors"
        verbose_name_plural = "Actors and Compositors"


class Genre(models.Model):
    name = models.CharField("Name", max_length=100)
    description = models.TextField("Description")
    url = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"


class Movie(models.Model):
    title = models.CharField("Title",max_length = 100)
    tagline = models.CharField("Tagline" , max_length = 100)
    description = models.TextField("Description")
    poster = models.ImageField("Poster", upload_to="movies/")
    year = models.PositiveSmallIntegerField("Year", default=2020)
    country = models.CharField("Country", max_length=30)
    directors = models.ManyToManyField(Actor, verbose_name="director", related_name="film_director")
    actors = models.ManyToManyField(Actor, verbose_name="actors", related_name="film_actors")
    genres = models.ManyToManyField(Genre, verbose_name="Genres")
    world_premiere = models.DateField("Premier in world", default=date.today)
    budget = models.PositiveIntegerField("Budget", default=0, help_text="sum in dollars")
    fees_in_usa = models.PositiveIntegerField("fees in USA", default=0, help_text="sum in dollars")
    fees_in_world = models.PositiveIntegerField("fees in World", default=0, help_text="sum in dollars")
    category = models.ForeignKey(Category, verbose_name="Category", on_delete=models.SET_NULL, null=True)
    url = models.SlugField(unique=True)
    draft = models.BooleanField("Черновик", default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"slug":self.url})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)
    class Meta:
        verbose_name = "Movie"
        verbose_name_plural = "Movies"


class MovieShots(models.Model):
    title = models.CharField("Title", max_length = 100)
    description = models.TextField("Description")
    image = models.ImageField("Picture", upload_to="movie_shots/")
    movie = models.ForeignKey(Movie, verbose_name="Movie ", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Movie Shot"
        verbose_name_plural = "Movie Shots"


class RatingStars(models.Model):
    value = models.PositiveSmallIntegerField("Value", default=0)

    def __str__(self):
        return str(self.value)

    class Meta:
        verbose_name = "Rating star"
        verbose_name_plural = " Rating Stars"
        ordering = ["-value"]


class Rating(models.Model):
    ip = models.CharField("IP addres", max_length=15)
    star = models.ForeignKey(RatingStars, on_delete=models.CASCADE, verbose_name="star")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="movies")

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"


class Reviews(models.Model):
    email = models.EmailField()
    name = models.CharField("Name", max_length=100)
    text = models.TextField("Messages", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="Parent", on_delete=models.SET_NULL, blank=True, null=True
    )
    movie = models.ForeignKey(Movie, verbose_name="movies", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
