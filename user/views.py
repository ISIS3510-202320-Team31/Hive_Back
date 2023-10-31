from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
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
def index_events_one(request, user_id, event_id):
    if request.method == 'POST':
        user = User.objects.get(id=user_id)
        event = Event.objects.get(id=event_id)
        event.participants.add(user)

        user_weights = user.weights.all()

        tags = event.tags.all()

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
