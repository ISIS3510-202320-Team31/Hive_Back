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
        return JsonResponse(event_data, safe=False, json_dumps_params={'indent': 4})

    if request.method == 'POST':
        data = json.loads(request.body)

        user = User.objects.get(pk=int(data['creator']))
        data['creator'] = user

        event = Event(**data)
        event.creator = user
        event.save()
        return JsonResponse({'message': 'Event created successfully'})

"""
@csrf_exempt
def index_detail(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return JsonResponse({'message': 'The event does not exist'}, status=404)

    if request.method == 'GET':
        # Serializa el objeto Event y convierte la representación JSON en un diccionario de Python
        event_data = json.loads(event.serialize())

        # Elimina la información del modelo y el campo 'pk'
        event_data = event_data[0]['fields']

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
"""