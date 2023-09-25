from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import User
from event.models import Event
#from event.models import Event
import json

# JSON format, CRUD

@csrf_exempt
def index_list(request):
    if request.method == 'GET':
        users = User.objects.all()
        events = Event.objects.all()
        users_data = list(users.values())

        # Get the events created by the user
        for user in users_data:
            events_participated = []
            user['events_created'] = list(Event.objects.filter(creator=user['id']).values())

            # Add the name of the creator to the event
            for event in user['events_created']:
                event['creator'] = User.objects.get(pk=event['creator_id']).name

            for event in events:
                participants = list(event.participants.values())
                for participant in participants:
                    if participant['id'] == user['id']:
                        event_p = {
                            'id': event.id,
                            'image': event.image,
                            'name': event.name,
                            'place': event.place,
                            'date': event.date,
                            'description': event.description,
                            'num_participants': event.num_participants,
                            'category': event.category,
                            'state': event.state,
                            'duration': event.duration,
                            'creator_id': event.creator.id,
                            'creator': event.creator.name,
                        }
                        events_participated.append(event_p)
            user['events_participated'] = events_participated



        return JsonResponse(users_data, safe=False, json_dumps_params={'indent': 4})

    if request.method == 'POST':
        data = json.loads(request.body)
        event = User(**data)
        event.save()
        return JsonResponse({'message': 'User created successfully'})
