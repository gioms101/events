from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


# Create your models here.
class MovieTheater(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Movie(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='movies')

    def __str__(self):
        return self.name


class Ticket(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='tickets')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    selected_ticket = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True,
                                        related_name='selected_tickets')
    theater = models.ForeignKey(MovieTheater, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateTimeField(default=datetime.now)
    row = models.PositiveIntegerField(default=0)
    seat = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
