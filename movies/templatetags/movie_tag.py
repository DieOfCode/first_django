from django import template
from movies.models import Category, Movie

register = template.Library()


@register.simple_tag
def get_categories():
    return Category.objects.all()


@register.inclusion_tag("movies/tags/last_movie.html")
def get_last_movie():
    movies = Movie.objects.order_by("id")[:5]
    return {"last_movies": movies}
