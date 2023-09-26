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
        event = User(**data)
        event.save()
        return JsonResponse({'message': 'User created successfully'})
    
    else:
        return JsonResponse({'message': 'The request must be a GET or POST'}, status=400)

@csrf_exempt
def index_one(request, user_id):
    if request.method == 'GET':
        user = User.objects.get(id=user_id)
        user_data = {
            'id': user.id,
            'icon': user.icon,
            'login': user.login,
            'name': user.name,
            'password': user.password,
            'email': user.email,
            'verificated': user.verificated,
            'role': user.role,
            'career': user.career,
            'birthdate': user.birthdate,
        }
        return JsonResponse(user_data, json_dumps_params={'indent': 4})
    
    elif request.method == 'DELETE':
        user = User.objects.get(id=user_id)
        user.delete()
        return JsonResponse({'message': 'User deleted successfully'})
    
    elif request.method == 'PUT':
        data = json.loads(request.body)
        user = User.objects.get(id=user_id)
        user.icon = data['icon']
        user.login = data['login']
        user.name = data['name']
        user.password = data['password']
        user.email = data['email']
        user.verificated = data['verificated']
        user.role = data['role']
        user.career = data['career']
        user.birthdate = data['birthdate']
        user.save()
        return JsonResponse({'message': 'User updated successfully'})
    
    else:
        return JsonResponse({'message': 'The request must be a GET, PUT or DELETE'}, status=400)

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
        return JsonResponse({'message': 'The request must be a GET'}, status=400)

@csrf_exempt
def index_events_one(request, user_id, event_id):
    if request.method == 'POST':
        user = User.objects.get(id=user_id)
        event = Event.objects.get(id=event_id)
        event.participants.add(user)
        event.save()
        return JsonResponse({'message': 'User added as participant successfully'})
    
    elif request.method == 'DELETE':
        user = User.objects.get(id=user_id)
        event = Event.objects.get(id=event_id)
        event.participants.remove(user)
        event.save()
        return JsonResponse({'message': 'User removed as participant successfully'})
    
    else:
        return JsonResponse({'message': 'The request must be a POST or DELETE'}, status=400)
