from django.contrib import admin
from .models import Movie, Ticket, MovieTheater

# Register your models here.

admin.site.register(Movie)
admin.site.register(Ticket)
admin.site.register(MovieTheater)
