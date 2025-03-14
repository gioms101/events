from rest_framework import serializers
from .models import Movie, Ticket


class ListEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ("id", "name", "location")


class RetrieveEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "name", 'price')
