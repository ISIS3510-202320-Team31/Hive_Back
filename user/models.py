from django.db import models

class Analista(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return 'Usuario %s' % (self.name)
