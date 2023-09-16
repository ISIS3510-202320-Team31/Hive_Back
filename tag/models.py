from django.db import models
from sqlalchemy import Column, String, Float
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.dialects.postgresql import UUID, ENUM, JSON
from enum import Enum

class Tag(models.Model):

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name