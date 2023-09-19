from django.db import models
from sqlalchemy import Column, String, Float
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.dialects.postgresql import UUID, ENUM, JSON
from enum import Enum
from tag.models import Tag

class Link(models.Model):

    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=1000)

    def __str__(self):
        return self.text
