from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import User
#from event.models import Event
import json

# JSON format, CRUD

@csrf_exempt
def index_list(request):
    if request.method == 'GET':
        users = User.objects.all()
        users_data = list(users.values())
        return JsonResponse(users_data, safe=False, json_dumps_params={'indent': 4})

    if request.method == 'POST':
        data = json.loads(request.body)
        event = User(**data)
        event.save()
        return JsonResponse({'message': 'User created successfully'})
