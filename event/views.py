from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core import serializers
from .models import Event
from .logic.EventForm import EventForm
import json

# JSON format, CRUD

@csrf_exempt
def index(request):
    try:
        if request.method == 'GET':
            #events = Event.objects.all()
            #data = serializers.serialize('json', events)
            #return JsonResponse(data, safe=False)
            return JsonResponse({'hola': 'si'})
        if request.method == 'POST':
            data = json.loads(request.body)
    except Exception as e:
        return JsonResponse({'error': str(e)})

