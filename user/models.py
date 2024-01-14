from django.db import models
from enum import Enum
from weight.models import Weight
import uuid

class User(models.Model):

    class Role(models.TextChoices):
        STUDENTS = "STUDENT"
        TEACHER = "TEACHER"
        ADMIN = "ADMIN"
        UNIANDES = "UNIANDES"

    class Career(models.TextChoices):
        ADMINISTRACION="ADMINISTRACION"
        ANTROPOLOGIA="ANTROPOLOGIA"
        ARQUITECTURA="ARQUITECTURA"
        ARTE="ARTE"
        BIOLOGIA="BIOLOGIA"
        CONTADURIA_INTERNACIONAL="CONTADURIA_INTERNACIONAL"
        DECANATURA_DE_ESTUDIANTES="DECANATURA_DE_ESTUDIANTES"
        DEPORTES="DEPORTES"
        DERECHO="DERECHO"
        DISENO="DISENO"
        ECONOMIA="ECONOMIA"
        EDUCACION="EDUCACION"
        FILOSOFIA="FILOSOFIA"
        FISICA="FISICA"
        GEOCIENCIAS="GEOCIENCIAS"
        ESCUELA_DE_GOBIERNO="ESCUELA_DE_GOBIERNO"
        HISTORIA="HISTORIA"
        HISTORIA_DEL_ARTE="HISTORIA_DEL_ARTE"
        INGENIERIA_BIOMEDICA="INGENIERIA_BIOMEDICA"
        INGENIERIA_CIVIL_Y_AMBIENTAL="INGENIERIA_CIVIL_Y_AMBIENTAL"
        INGENIERIA_DE_ALIMENTOS="INGENIERIA_DE_ALIMENTOS"
        INGENIERIA_DE_SISTEMAS_Y_COMPUTACION="INGENIERIA_DE_SISTEMAS_Y_COMPUTACION"
        INGENIERIA_ELECTRICA_Y_ELECTRONICA="INGENIERIA_ELECTRICA_Y_ELECTRONICA"
        INGENIERIA_INDUSTRIAL="INGENIERIA_INDUSTRIAL"
        INGENIERIA_MECANICA="INGENIERIA_MECANICA"
        INGENIERIA_QUIMICA="INGENIERIA_QUIMICA"
        LENGUAS_Y_CULTURA="LENGUAS_Y_CULTURA"
        LITERATURA="LITERATURA"
        MATEMATICAS="MATEMATICAS"
        MEDICINA="MEDICINA"
        MICROBIOLOGIA="MICROBIOLOGIA"
        MUSICA="MUSICA"
        NARRATIVAS_DIGITALES="NARRATIVAS_DIGITALES"
        PSICOLOGIA="PSICOLOGIA"
        QUIMICA="QUIMICA"
        OTRO="OTRO"

    id = models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False)
    icon = models.CharField(max_length=50)
    login = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    verificated = models.BooleanField(default=False)
    role = models.CharField(max_length=10,choices=Role.choices,default=Role.STUDENTS)
    career = models.CharField(max_length=50,choices=Career.choices,default=Career.OTRO)
    birthdate = models.DateField()
    friends = models.ManyToManyField("self",blank=True)
    #tags = models.ManyToManyField(Tag,blank=True)
    weights = models.ManyToManyField(Weight,blank=True)

    def __str__(self):
        return self.name
