from django.db.models.aggregates import Sum
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters import rest_framework as filters
from .models import Movie, Ticket
from .serializers import ListEventSerializer, RetrieveEventSerializer, TicketSerializer
from .cfilters import MovieFilter


class EventModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Movie.objects.select_related('category').prefetch_related('theater', 'date').all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MovieFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return ListEventSerializer
        elif self.action == 'retrieve':
            return RetrieveEventSerializer

    @action(
        detail=True,
        serializer_class=TicketSerializer,
    )
    def tickets(self, request, pk=None):
        serializer = self.serializer_class(Ticket.objects.filter(event_id=pk), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TotalPriceAPIView(GenericAPIView):
    """
    API endpoint to compute the total sum of the user's selected seats.

    Returns:
        - total_sum (int or float): The total price of the selected seats.
    """
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, *args, **kwargs):
        return Response({"total_sum": Ticket.objects.filter(selected_ticket_id=request.user.id)
                        .aggregate(total_sum=Sum('price'))}['total_sum'])
