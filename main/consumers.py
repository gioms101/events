import json
from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken
from .models import Ticket


class EventConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        query_params = parse_qs(self.scope["query_string"].decode())

        self.event_id = self.scope['url_route']['kwargs']['pk']
        date = query_params.get("date", [None])[0]
        theater = query_params.get("theater", [None])[0]

        if not all([self.event_id, date, theater]):
            await self.close()
            return

        self.room_name = f'events_{self.event_id}_{date}_{theater}'  # This is going to be room name Where user can
                                                                     # select tickets.
        token = query_params.get("token", [None])[0]
        if token:
            self.user = await self.get_user(token)
            if not self.user:
                await self.close()
                return
        else:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        ticket_id = json.loads(text_data)['ticket_id']

        ticket_status = await self.select_ticket(ticket_id, self.event_id)

        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'ticket_message',
                'ticket_status': ticket_status,
                'ticket_id': ticket_id,
            }
        )

    async def ticket_message(self, event):
        ticket_id = event['ticket_id']
        ticket_status = event['ticket_status']

        await self.send(text_data=json.dumps({
            'ticket_status': ticket_status,
            'ticket_id': ticket_id,
        }))

    @database_sync_to_async
    def get_user(self, token):
        """Fetch user from JWT token"""
        try:
            decoded_token = AccessToken(token)
            return User.objects.prefetch_related('selected_ticket').get(id=decoded_token["user_id"])
        except Exception:
            return None

    @database_sync_to_async
    def select_ticket(self, ticket_id, event_id):

        if self.user.selected_ticket.all().count() > 4:
            return "Can't select more than 4 tickets"

        ticket = Ticket.objects.select_for_update().filter(id=ticket_id, event_id=event_id)
        if ticket.exists():
            ticket = ticket.first()
            if ticket.selected_ticket == self.user:
                ticket.selected_ticket = None
                ticket.save(update_fields=['selected_ticket'])
                return "Ticket selection removed!"
            elif not ticket.selected_ticket:
                ticket.selected_ticket = self.user
                ticket.save(update_fields=['selected_ticket'])
                return "Ticket selection added!"
            else:
                return "Ticket already selected!"
        else:
            return "Ticket not found"
