from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core import serializers
from .models import Event
from user.models import User
from .logic.EventForm import EventForm
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
    


