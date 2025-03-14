from django_filters import rest_framework as filters
from .models import Movie, MovieTheater
from django.db.models.functions import TruncDate, ExtractHour


class MovieFilter(filters.FilterSet):
    theater = filters.ModelMultipleChoiceFilter(
        field_name='theater',
        queryset=MovieTheater.objects.all(),
    )
    date_only = filters.DateFilter(field_name="date__date", method='filter_date_only')

    category_name = filters.CharFilter(
        field_name='category__slug',
    )

    class Meta:
        model = Movie
        fields = ("theater",)

    @staticmethod
    def filter_date_only(queryset, name, value):
        return queryset.annotate(
            truncated_date=TruncDate('date__date')
        ).filter(truncated_date=value)
