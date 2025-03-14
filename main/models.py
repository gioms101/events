from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class MovieTheater(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Movie(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    date = models.DateTimeField()
    theater = models.ManyToManyField(MovieTheater, related_name='movies')

    def __str__(self):
        return self.name


class Ticket(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='tickets')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    selected_ticket = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True,
                                        related_name='selected_tickets')

    def __str__(self):
        return self.name
