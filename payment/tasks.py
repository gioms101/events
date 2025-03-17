from main.models import Ticket
from celery import shared_task



@shared_task
def save_tickets(event_id, user_id):
    selected_tickets = Ticket.objects.filter(event_id=event_id, selected_ticket=user_id)
    for ticket in selected_tickets:
        ticket.user_id = user_id
        ticket.selected_ticket = None
        ticket.save(update_fields=["user_id", 'selected_ticket'])


@shared_task
def remove_user(event_id, user_id):
    tickets = Ticket.objects.filter(event_id=event_id, selected_ticket=user_id)
    for ticket in tickets:
        ticket.user_id = None
        ticket.save(update_fields=['user_id'])
