from django.db import models
from enum import Enum
from tag.models import Tag
import uuid

class Weight(models.Model):
    id = models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False)
    value = models.IntegerField()
    tag = models.ForeignKey('tag.Tag', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}"
 