from django.db import models
from sqlalchemy import Column, String, Float
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.dialects.postgresql import UUID, ENUM, JSON
from enum import Enum
from user.models import User
from tag.models import Tag

class Event(models.Model):
    _DATABASE = 'remotedata'
    class Category(models.TextChoices):
        ACADEMIC="ACADEMIC"
        CULTURAL="CULTURAL"
        SPORTS="SPORTS"
        ENTERTAINMENT="ENTERTAINMENT"
        OTHER="OTHER"

    id = models.AutoField(primary_key=True)
    image = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    place = models.CharField(max_length=50)
    date = models.DateField()
    description = models.CharField(max_length=50)
    num_participants = models.IntegerField() 
    links = models.CharField(max_length=1000)
    category = models.CharField(max_length=20,choices=Category.choices,default=Category.OTHER)
    state = models.BooleanField(default=True)
    duration = models.IntegerField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, related_name='participants')
    tags = models.ManyToManyField(Tag, related_name='tags')

    def __str__(self):
        return self.name