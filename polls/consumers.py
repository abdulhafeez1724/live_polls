import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Poll, Choice

class PollConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = 'live_poll'
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        choice_id = data['choice_id']
        choice = Choice.objects.get(id=choice_id)
        choice.votes += 1
        choice.save()

        poll = choice.poll
        choices = poll.choices.all()
        result = [{'choice_text': c.choice_text, 'votes': c.votes} for c in choices]

        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'update_poll',
                'results': result,
            }
        )

    def update_poll(self, event):
        self.send(text_data=json.dumps({
            'results': event['results'],
        }))
