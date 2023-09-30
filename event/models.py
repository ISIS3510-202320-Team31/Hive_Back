from django.db import models
from enum import Enum
from user.models import User
from tag.models import Tag
from link.models import Link
import uuid

class Event(models.Model):
    class Category(models.TextChoices):
        ACADEMIC="ACADEMIC"
        CULTURAL="CULTURAL"
        SPORTS="SPORTS"
        ENTERTAINMENT="ENTERTAINMENT"
        OTHER="OTHER"

    id = models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False)
    image = models.CharField(max_length=1000)
    name = models.CharField(max_length=50)
    place = models.CharField(max_length=50)
    date = models.DateField()
    description = models.CharField(max_length=1000)
    num_participants = models.IntegerField(null = True) 
    category = models.CharField(max_length=20,choices=Category.choices,default=Category.OTHER)
    state = models.BooleanField(default=True)
    duration = models.IntegerField(null = True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, related_name='participants')
    tags = models.ManyToManyField(Tag, related_name='tags')
    links = models.ManyToManyField(Link, related_name='links')

    def __str__(self):
        return self.name