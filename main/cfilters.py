from django_filters import rest_framework as filters
from .models import Movie, Ticket


class MovieFilter(filters.FilterSet):

    category_name = filters.CharFilter(
        field_name='category__slug',
    )

    class Meta:
        model = Movie
        fields = ('category_name',)


class TicketFilter(filters.FilterSet):

    date = filters.DateTimeFilter(field_name="date")
    theater = filters.CharFilter(field_name="theater__name", lookup_expr="iexact")

    class Meta:
        model = Ticket
        fields = ("date", 'theater')

