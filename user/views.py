from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db import connection
from .models import User
from event.models import Event
from weight.models import Weight
import json
from utils.utils import convert_to_json, assign_from_dict

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
            user['events_created'] = []

            # Add in events created the IDs of the events created by the user
            for event in events:
                if event.creator.id == user['id']:
                    user['events_created'].append(event.id)
                
                participants = list(event.participants.values())
                for participant in participants:
                    if participant['id'] == user['id']:
                        event_p = event.id
                        events_participated.append(event_p)
            user['events_participated'] = events_participated
        return JsonResponse(users_data, safe=False, json_dumps_params={'indent': 4})

    elif request.method == 'POST':
        data = json.loads(request.body)
        user = User(**data)
        user.save()
        user_data = convert_to_json(user)
        return JsonResponse(user_data, json_dumps_params={'indent': 4}, status=201)
    
    else:
        return JsonResponse({'message': 'La solicitud debe ser un GET o POST'}, status=400)

@csrf_exempt
def index_one(request, user_id):
    if request.method == 'GET':
        user = User.objects.get(id=user_id)
        user_data = convert_to_json(user)
        return JsonResponse(user_data, json_dumps_params={'indent': 4})
    
    elif request.method == 'PUT':
        data = json.loads(request.body)
        user = User.objects.get(id=user_id)
        assign_from_dict(user, data)
        user.save()
        user_data = convert_to_json(user)
        return JsonResponse(user_data, json_dumps_params={'indent': 4})
    
    elif request.method == 'DELETE':
        user = User.objects.get(id=user_id)
        user.delete()
        return JsonResponse({'message': f'Usuario {user_id} eliminado correctamente'})
    
    else:
        return JsonResponse({'message': 'La solicitud debe ser un GET, PUT o DELETE'}, status=400)

@csrf_exempt
def index_events_list(request, user_id):
    if request.method == 'GET':
        user = User.objects.get(id=user_id)
        events = Event.objects.all()
        events_data = []

        for event in events:
            # all events where user is creator or participant
            if event.creator.id == user.id or user in event.participants.all():
                events_data.append(event.id)
        
        return JsonResponse(events_data, safe=False, json_dumps_params={'indent': 4})
    
    else:
        return JsonResponse({'message': 'La solicitud debe ser un GET'}, status=400)
    
@csrf_exempt
def index_events_list_created(request, user_id):
    if request.method == 'GET':
        events = Event.objects.all()
        events_data = list(events.values())
        events_filtered = []

        for event in events_data:
            if event['creator_id'] == user_id:
                links_complete = []
                tags_complete = []
                participants_complete = []
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
                event['creator'] = User.objects.get(pk=event['creator_id']).name
                events_filtered.append(event)
        
        return JsonResponse(events_filtered, safe=False, json_dumps_params={'indent': 4})
    
    else:
        return JsonResponse({'message': 'La solicitud debe ser un GET'}, status=400)

@csrf_exempt
def index_events_one(request, user_id, event_id):
    if request.method == 'POST':
        user = User.objects.get(id=user_id)
        event = Event.objects.get(id=event_id)
        event.participants.add(user)

        user_weights = user.weights.all()

        tags = event.tags.all()

        print(f"Adding user {user_id} to event {event_id}")

        for tag in tags:
            # if the user has a weight for the tag, add 1 to the value
            for weight in user_weights:
                if weight.tag.id == tag.id:
                    weight.value += 1
                    weight.save()
                    break
            # if the user does not have a weight for the tag, create one
            else:
                weight = Weight(user=user, tag=tag, value=1)
                weight.save()
                user.weights.add(weight)
                user.save()
            
        event.save()
        new_event = convert_to_json(event)
        new_event['participants'] = [participant['id'] for participant in list(event.participants.values())]
        new_event['tags'] = [tag['name'] for tag in list(event.tags.values())]
        new_event['links'] = [link['text'] for link in list(event.links.values())]
        new_event['creator_id'] = new_event['creator']['id']
        new_event['creator'] = new_event['creator']['name']

        print("Evento actualizado:")
        print(new_event)

        return JsonResponse(new_event,safe=False, json_dumps_params={'indent': 4})
        # return JsonResponse({'message': f'User {user_id} added as participant of event {event_id} successfully'})
    
    elif request.method == 'DELETE':
        user = User.objects.get(id=user_id)
        event = Event.objects.get(id=event_id)
        event.participants.remove(user)
        event.save()

        new_event = convert_to_json(event)
        new_event['participants'] = [participant['id'] for participant in list(event.participants.values())]
        new_event['tags'] = [tag['name'] for tag in list(event.tags.values())]
        new_event['links'] = [link['text'] for link in list(event.links.values())]
        new_event['creator_id'] = new_event['creator']['id']
        new_event['creator'] = new_event['creator']['name']

        return JsonResponse(new_event,safe=False, json_dumps_params={'indent': 4})
        # return JsonResponse({'message': f'User {user_id} removed as participant of event {event_id} successfully'})
    
    else:
        return JsonResponse({'message': 'La solicitud debe ser un POST o DELETE'}, status=400)


@csrf_exempt
def index_user_register(request):
    
    # Register of the user in the database
    if request.method == "POST":
        data = json.loads(request.body)

        # Create dict with data of the user
        user_data = {
            'icon': "icon",
            'login': data['login'],
            'name': data['name'],
            'password': data['password'],
            'email': data['email'],
            'career': data['career'],
            'birthdate': data['birthdate']
        }

        # Check if any user has the same login
        users = User.objects.all()

        for user in users:
            if user.login == user_data['login']:
                return JsonResponse({'message': 'El login ya existe'}, status=400)
            if user.email == user_data['email']:
                return JsonResponse({'message': 'El email ya existe'}, status=400)

        # Create user
        user = User(**user_data)
        user.save()
        user_data = convert_to_json(user)

        # Remove password from response
        user_data.pop('password')

        return JsonResponse(user_data, json_dumps_params={'indent': 4}, status=201)

@csrf_exempt
def index_user_login(request):
    # Login of the user in the database
    if request.method == "POST":
        data = json.loads(request.body)

        # Create dict with data of the user
        user_data = {
            'login': data['login'],
            'password': data['password']
        }

        # Check if any user has the same login
        users = User.objects.all()

        for user in users:
            if user.login == user_data['login']:
                if user.password == user_data['password']:
                    user_data = convert_to_json(user)
                    user_data.pop('password')
                    return JsonResponse(user_data, json_dumps_params={'indent': 4}, status=201)
                else:
                    return JsonResponse({'message': 'Contraseña incorrecta'}, status=400)

        return JsonResponse({'message': 'El login no existe'}, status=400)

@csrf_exempt
def index_top_creators(request):
    if request.method == 'GET':
        # Get the top 5 creators of events (Their name and the average of attendees of their events)
        
        raw_query = """
            WITH CreatorWithMoreThan3 AS (
            SELECT
                uu.id AS creator_id,
                uu.name AS creator_name,
                COUNT(uu.id) AS event_count
            FROM
                user_user uu
                JOIN event_event ee ON uu.id = ee.creator_id
            GROUP BY
                uu.id
            HAVING
                COUNT(uu.id) >= 3
        )

        , AverageParticipants AS (
            SELECT
                c.creator_id,
                AVG(ep.num_participants) AS avg_participants
            FROM
                CreatorWithMoreThan3 c
                JOIN event_event ee ON c.creator_id = ee.creator_id
                LEFT JOIN (
                    SELECT
                        event_id,
                        COUNT(user_id) AS num_participants
                    FROM
                        event_event_participants
                    GROUP BY
                        event_id
                ) ep ON ee.id = ep.event_id
            GROUP BY
                c.creator_id
        )

        SELECT
            ap.creator_id,
            c.creator_name,
            ap.avg_participants
        FROM
            AverageParticipants ap
            JOIN CreatorWithMoreThan3 c ON ap.creator_id = c.creator_id
        ORDER BY
            ap.avg_participants DESC
        LIMIT 5"""
        
        with connection.cursor() as cursor:
            cursor.execute(raw_query)
            top_creators = cursor.fetchall()

        top_creators = [{'name': creator[1], 'average': creator[2]} for creator in top_creators]

        return JsonResponse(top_creators, safe=False, json_dumps_params={'indent': 4})

    
    else:
        return JsonResponse({'message': 'La solicitud debe ser un GET'}, status=400)

@csrf_exempt
#Get the top five partners of the events that an user attends
def index_top_partners(request, user_id):
    if request.method == 'GET':
        #Get events of the user
        user_events = Event.objects.filter(participants=user_id)
        
        #Get participants of the events
        top_partners = {}
        for event in user_events:
            participants = event.participants.exclude(id=user_id)
            for participant in participants:
                if participant.id in top_partners:
                    top_partners[participant.id] += 1
                else:
                    top_partners[participant.id] = 1

        #Sort the partners by the number of events that the user and the partner had attended
        top_partners = sorted(top_partners.items(), key=lambda x: x[1], reverse=True)

        #Get the name of the top five partners in a list
        top_partners_names = []
        i = 0
        while i < len(top_partners) and i < 5:
            partner_id = top_partners[i][0]
            partner_name = get_object_or_404(User, id=partner_id).name
            top_partners_names.append(partner_name)
            i += 1
        
        return JsonResponse(top_partners_names, safe=False, json_dumps_params={'indent': 4})

    else:
        return JsonResponse({'message': 'La solicitud debe ser un GET'}, status=400)







            

        

        


