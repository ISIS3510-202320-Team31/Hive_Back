from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Weight
import json

# JSON format, CRUD

@csrf_exempt
def index_list(request):
    if request.method == 'GET':
        weights = Weight.objects.all()
        weights_data = weights.values()
        return JsonResponse(list(weights_data), safe=False, json_dumps_params={'indent': 4})

    if request.method == 'POST':
        body = json.loads(request.body)
        weight = Weight.objects.create(value=body['value'], user_id=body['user_id'], tag_id=body['tag_id'])
        return JsonResponse({'id': str(weight.id)}, status=201)

@csrf_exempt
def index_detail(request, id):
    try:
        weight = Weight.objects.get(id=id)
    except Weight.DoesNotExist:
        return JsonResponse({'error': 'Weight not found'}, status=404)

    if request.method == 'GET':
        weight_data = {
            'id': str(weight.id),
            'value': weight.value,
            'user_id': str(weight.user_id),
            'tag_id': str(weight.tag_id)
        }
        return JsonResponse(weight_data, json_dumps_params={'indent': 4})

    if request.method == 'PUT':
        body = json.loads(request.body)
        weight.value = body['value']
        weight.user_id = body['user_id']
        weight.tag_id = body['tag_id']
        weight.save()
        return JsonResponse({'message': 'Weight updated successfully!'}, status=200)

    if request.method == 'DELETE':
        weight.delete()
        return JsonResponse({'message': 'Weight deleted successfully!'}, status=200)

@csrf_exempt
def index_user(request, user_id):
    if request.method == 'GET':
        weights = Weight.objects.filter(user_id=user_id)
        weights_data = weights.values()
        return JsonResponse(list(weights_data), safe=False, json_dumps_params={'indent': 4})

@csrf_exempt
def index_tag(request, tag_id):
    if request.method == 'GET':
        weights = Weight.objects.filter(tag_id=tag_id)
        weights_data = weights.values()
        return JsonResponse(list(weights_data), safe=False, json_dumps_params={'indent': 4})
