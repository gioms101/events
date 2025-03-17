from django.contrib.auth.models import User
from rest_framework import permissions


class IsValidToRefund(permissions.BasePermission):
    message = "You can't request to refund. The event starts in less than 3 hours."

    def has_object_permission(self, request, view, obj):

        event_starting_date = obj.event.date
        transaction_creation_time = obj.created_at
        time_diff = transaction_creation_time.start_time - event_starting_date.created_at
        return time_diff.total_seconds() / 3600 >= 3


class CanBuyTicket(permissions.BasePermission):
    message = "You can't buy more than 4 tickets on the same event!"

    def has_permission(self, request, view):
        user = User.objects.prefetch_related("tickets", 'selected_ticket').get(id=request.user.id)
        total_amount_of_tickets = user.selected_ticket.all().count() + user.tickets.all().count()
        return total_amount_of_tickets <= 4

