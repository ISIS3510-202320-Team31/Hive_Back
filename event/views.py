from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Event
from user.models import User
import json

# JSON format, CRUD

@csrf_exempt
def index_list(request):
    if request.method == 'GET':
        events = Event.objects.all()
        event_data = list(events.values())
        
        # Add the creator name to the event
        for event in event_data:
            links_complete = []
            tags_complete = []
            participants_complete = []
            event['creator'] = User.objects.get(pk=event['creator_id']).name
            indiv_event = Event.objects.get(pk=event['id'])
            
            # Add the participants, tags and links to the event, but only their ids
            # The frontend will have to make a request to get the data of each participant, tag and link
            participants = list(indiv_event.participants.values())
            tags = list(indiv_event.tags.values())
            links = list(indiv_event.links.values())

            for participant in participants:
                participants_complete.append(participant['id'])
            for tag in tags:
                tags_complete.append(tag['id'])
            for link in links:
                links_complete.append(link['id'])
            
            event['participants'] = participants_complete
            event['tags'] = tags_complete
            event['links'] = links_complete

        return JsonResponse(event_data, safe=False, json_dumps_params={'indent': 4})

    if request.method == 'POST':
        data = json.loads(request.body)

        user = User.objects.get(pk=data['creator'])
        data['creator'] = user

        event = Event(**data)
        event.creator = user
        event.save()
        return JsonResponse({'message': 'Event created successfully'})

@csrf_exempt
def index_detail(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return JsonResponse({'message': 'The event does not exist'}, status=404)

    if request.method == 'GET':
        
        # Transform event into JSON format 
        event_data = {
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
            'creator': event.creator.name,
            'participants': list(event.participants.values()),
            'tags': list(event.tags.values()),
            'links': list(event.links.values())
        }

        return JsonResponse(event_data, safe=False, json_dumps_params={'indent': 4})

    if request.method == 'PUT':
        data = json.loads(request.body)

        user = User.objects.get(pk=int(data['creator']))
        data['creator'] = user

        event = Event(**data)
        event.creator = user
        event.save()
        return JsonResponse({'message': 'Event updated successfully'})

    if request.method == 'DELETE':
        event.delete()
        return JsonResponse({'message': 'Event deleted successfully'})
    
@csrf_exempt
def index_participants(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return JsonResponse({'message': 'The event does not exist'}, status=404)

    if request.method == 'GET':
        participants = list(event.participants.values())
        return JsonResponse(participants, safe=False, json_dumps_params={'indent': 4})

    if request.method == 'POST':
        data = json.loads(request.body)
        user = User.objects.get(pk=data['id_participant'])
        event.participants.add(user)
        event.save()
        return JsonResponse({'message': 'Participant added successfully'})
