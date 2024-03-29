from django.db import models
from enum import Enum
import uuid

class Tag(models.Model):
    id = models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name