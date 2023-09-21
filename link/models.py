from django.db import models
from sqlalchemy import Column, String, Float
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.dialects.postgresql import UUID, ENUM, JSON
from enum import Enum
from tag.models import Tag
import uuid

class Link(models.Model):

    id = models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False)
    text = models.CharField(max_length=1000)

    def __str__(self):
        return self.text
