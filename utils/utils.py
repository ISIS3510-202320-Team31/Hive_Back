from django.db import models

""" A method that converts an instance to a dictionary, like this:
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

or

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
"""
def convert_to_json(instance):
    model_data = {}
    for field in type(instance)._meta.fields:
        model_data[field.name] = getattr(instance, field.name)
        if isinstance(type(model_data[field.name]), type(models.Model)):
            model_data[field.name] = convert_to_json(model_data[field.name])
    return model_data

""" A method that assigns from a dictionary to an instance, like this:

        user.icon = data['icon']
        user.login = data['login']
        user.name = data['name']
        user.password = data['password']
        user.email = data['email']
        user.verificated = data['verificated']
        user.role = data['role']
        user.career = data['career']
        user.birthdate = data['birthdate']
"""
def assign_from_dict(instance, data):
    for field in type(instance)._meta.fields:
        # only update fields that are in the data
        if field.name in data:
            setattr(instance, field.name, data[field.name])
