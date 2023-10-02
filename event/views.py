from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Event
from user.models import User
from tag.models import Tag
from link.models import Link
import json
from utils.utils import convert_to_json, assign_from_dict
from sortedcontainers import SortedList


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
                tags_complete.append(tag['name'])
            for link in links:
                links_complete.append(link['text'])
            
            event['participants'] = participants_complete
            event['tags'] = tags_complete
            event['links'] = links_complete

        return JsonResponse(event_data, safe=False, json_dumps_params={'indent': 4})

    elif request.method == 'POST':
        data = json.loads(request.body)

        # Get the user object from the id
        user = User.objects.get(pk=data['creator'])
        data['creator'] = user

        # For each tag, get the object from the name, if it doesn't exist, create it
        tags = data['tags']
        del data['tags']
        tags_object = []
        for tag in tags:
            tag_object, created = Tag.objects.get_or_create(name=tag)
            tags_object.append(tag_object)
        
        # For each link, get the object from the text, if it doesn't exist, create it
        links = data['links']
        del data['links']
        links_object = []
        for link in links:
            link_object, created = Link.objects.get_or_create(text=link)
            links_object.append(link_object)

        event = Event(**data)
        event.creator = user
        event.save()

        # Add the tags and links to the event
        event.tags.set(tags_object)
        event.links.set(links_object)

        event_data = convert_to_json(event)
        event_data['creator'] = event_data['creator']['id']

        return JsonResponse(event_data, json_dumps_params={'indent': 4}, status=201)

    else:
        return JsonResponse({'message': 'The request must be a GET or POST'}, status=400)


@csrf_exempt
def events_for_user(request,user_id):
    if request.method == 'GET':
        user = User.objects.get(id=user_id)
        weights = user.weights.all()
        events = Event.objects.all()
        event_data = list(events.values())
        sorted_events = SortedList( key=lambda x: -x['score'])
        tag_weight = {}
        events_for_user = []
        for weight in weights:
            tag_weight[weight.tag.name.lower()] = weight.value
        # Add the creator name to the event
        for event in event_data:
            if event['date']<datetime.now().date():
                continue
            tags_complete = []
            participants_complete = []
            event['creator'] = User.objects.get(pk=event['creator_id']).name
            indiv_event = Event.objects.get(pk=event['id'])
            
            # Add the participants, tags and links to the event, but only their ids
            # The frontend will have to make a request to get the data of each participant, tag and link
            participants = list(indiv_event.participants.values())
            tags = list(indiv_event.tags.values())
            links = [link['text'] for link in indiv_event.links.values()]
            score = 0

            for participant in participants:
                participants_complete.append(participant['id'])
                
            for tag in tags:
                tag_name = tag['name']
                if tag_name in tag_weight:
                    score += tag_weight[tag_name]
                tags_complete.append(tag_name)
                
            event['participants'] = participants_complete
            event['tags'] = tags_complete
            event['links'] = links
            sorted_events.add({'score':score,'event':event})
        for event in sorted_events:
            events_for_user.append(event['event'])
        return JsonResponse(events_for_user, safe=False, json_dumps_params={'indent': 4})

@csrf_exempt
def index_detail(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return JsonResponse({'message': 'The event does not exist'}, status=404)

    if request.method == 'GET':
        # Transform event into JSON format 
        event_data = convert_to_json(event)
        event_data['participants'] = list(event.participants.values())
        event_data['tags'] = list(event.tags.values())
        event_data['links'] = list(event.links.values())
        event_data['creator_id'] = event_data['creator']['id']
        event_data['creator'] = event_data['creator']['name']

        # Change tag object for only the name and link object for only the text
        tag_complete = []
        for tag in event_data['tags']:
            tag.pop('id')
            tag_complete.append(tag['name'])
        event_data['tags'] = tag_complete

        link_complete = []
        for link in event_data['links']:
            link.pop('id')
            link_complete.append(link['text'])
        
        event_data['links'] = link_complete

        participants_complete = []
        for participant in event_data['participants']:
            participant.pop('name')
            participant.pop('icon')
            participant.pop('login')
            participant.pop('password')
            participant.pop('email')
            participant.pop('verificated')
            participant.pop('role')
            participant.pop('career')
            participant.pop('birthdate')
            participants_complete.append(participant['id'])

        event_data['participants'] = participants_complete
        

        return JsonResponse(event_data, safe=False, json_dumps_params={'indent': 4})

    elif request.method == 'PUT':
        data = json.loads(request.body)
        event = Event.objects.get(id=pk)

        user = User.objects.get(pk=data['creator'])
        data['creator'] = user

        # For each tag, get the object from the name, if it doesn't exist, create it
        tags = data['tags']
        del data['tags']
        tags_object = []
        for tag in tags:
            tag_object, created = Tag.objects.get_or_create(name=tag)
            tags_object.append(tag_object)
        
        # For each link, get the object from the text, if it doesn't exist, create it
        links = data['links']
        del data['links']
        links_object = []
        for link in links:
            link_object, created = Link.objects.get_or_create(text=link)
            links_object.append(link_object)

        assign_from_dict(event, data)
        event.creator = user
        event.save()

        # Add the tags and links to the event
        event.tags.set(tags_object)
        event.links.set(links_object)

        event_data = convert_to_json(event)
        return JsonResponse(event_data, json_dumps_params={'indent': 4})

    elif request.method == 'DELETE':
        event.delete()
        return JsonResponse({'message': f'Event {pk} deleted successfully'})

    else:
        return JsonResponse({'message': 'The request must be a GET, PUT or DELETE'}, status=400)

#Get all the events order by date
@csrf_exempt
def index_list_by_date(request, date):    
    if request.method == 'GET':
        events = Event.objects.filter(date__gte=date).order_by('date')
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
                tags_complete.append(tag['name'])
            for link in links:
                links_complete.append(link['text'])
            
            event['participants'] = participants_complete
            event['tags'] = tags_complete
            event['links'] = links_complete

        return JsonResponse(event_data, safe=False, json_dumps_params={'indent': 4})
        
    else:
        return JsonResponse({'message': 'The request must be a GET or POST'}, status=400)

@csrf_exempt
def index_list_by_date_and_user(request, date, user_id, future):
    if request.method == 'GET':
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return JsonResponse({'message': 'User not found'}, status=404)
        

        if future == '1':
            #Check if the user is a participant of the event
            events = Event.objects.filter(date__gte=date, participants__id=user_id).order_by('date')

            
        elif future == '0':
            try:
                input_date = datetime.strptime(date, '%Y-%m-%d')
                date_before = input_date - timedelta(days=1)
                str_date_before = date_before.strftime('%Y-%m-%d')

                events = Event.objects.filter(date__lte=str_date_before, participants__id=user_id).order_by('-date')

            except ValueError:
                return JsonResponse({'message': 'The date must be in the format YYYY-MM-DD'}, status=400)

            

           
        
        event_data = list(events.values())

        for event in event_data:
            links_complete = []
            tags_complete = []
            participants_complete = []
            event['creator'] = User.objects.get(pk=event['creator_id']).name
            indiv_event = Event.objects.get(pk=event['id'])
            
            participants = list(indiv_event.participants.values())
            tags = list(indiv_event.tags.values())
            links = list(indiv_event.links.values())

            for participant in participants:
                participants_complete.append(participant['id'])
            for tag in tags:
                tags_complete.append(tag['name'])
            for link in links:
                links_complete.append(link['text'])
            
            event['participants'] = participants_complete
            event['tags'] = tags_complete
            event['links'] = links_complete

        return JsonResponse(event_data, safe=False, json_dumps_params={'indent': 4})
        
    else:
        return JsonResponse({'message': 'The request must be a GET or POST'}, status=400)