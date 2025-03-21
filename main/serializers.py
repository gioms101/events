from rest_framework import serializers
from .models import Movie, Ticket


class ListEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ("id", "name")


class RetrieveEventSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')

    class Meta:
        model = Movie
        fields = ("category",)


class TicketSerializer(serializers.ModelSerializer):
    theater = serializers.CharField(source="theater.name")

    class Meta:
        model = Ticket
        fields = ("id", "name", 'price', "theater", "date")
