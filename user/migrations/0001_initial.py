# Generated by Django 4.2 on 2023-09-19 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("tag", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("icon", models.CharField(max_length=50)),
                ("login", models.CharField(max_length=50)),
                ("name", models.CharField(max_length=50)),
                ("password", models.CharField(max_length=50)),
                ("email", models.CharField(max_length=50)),
                ("verificated", models.BooleanField(default=False)),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("STUDENT", "Students"),
                            ("TEACHER", "Teacher"),
                            ("ADMIN", "Admin"),
                            ("UNIANDES", "Uniandes"),
                        ],
                        default="STUDENT",
                        max_length=10,
                    ),
                ),
                (
                    "career",
                    models.CharField(
                        choices=[
                            ("ADMINISTRACION", "Administracion"),
                            ("ANTROPOLOGIA", "Antropologia"),
                            ("ARQUITECTURA", "Arquitectura"),
                            ("ARTE", "Arte"),
                            ("BIOLOGIA", "Biologia"),
                            ("CONTADURIA_INTERNACIONAL", "Contaduria Internacional"),
                            ("DECANATURA_DE_ESTUDIANTES", "Decanatura De Estudiantes"),
                            ("DEPORTES", "Deportes"),
                            ("DERECHO", "Derecho"),
                            ("DISENO", "Diseno"),
                            ("ECONOMIA", "Economia"),
                            ("EDUCACION", "Educacion"),
                            ("FILOSOFIA", "Filosofia"),
                            ("FISICA", "Fisica"),
                            ("GEOCIENCIAS", "Geociencias"),
                            ("ESCUELA_DE_GOBIERNO", "Escuela De Gobierno"),
                            ("HISTORIA", "Historia"),
                            ("HISTORIA_DEL_ARTE", "Historia Del Arte"),
                            ("INGENIERIA_BIOMEDICA", "Ingenieria Biomedica"),
                            (
                                "INGENIERIA_CIVIL_Y_AMBIENTAL",
                                "Ingenieria Civil Y Ambiental",
                            ),
                            ("INGENIERIA_DE_ALIMENTOS", "Ingenieria De Alimentos"),
                            (
                                "INGENIERIA_DE_SISTEMAS_Y_COMPUTACION",
                                "Ingenieria De Sistemas Y Computacion",
                            ),
                            (
                                "INGENIERIA_ELECTRICA_Y_ELECTRONICA",
                                "Ingenieria Electrica Y Electronica",
                            ),
                            ("INGENIERIA_INDUSTRIAL", "Ingenieria Industrial"),
                            ("INGENIERIA_MECANICA", "Ingenieria Mecanica"),
                            ("INGENIERIA_QUIMICA", "Ingenieria Quimica"),
                            ("LENGUAS_Y_CULTURA", "Lenguas Y Cultura"),
                            ("LITERATURA", "Literatura"),
                            ("MATEMATICAS", "Matematicas"),
                            ("MEDICINA", "Medicina"),
                            ("MICROBIOLOGIA", "Microbiologia"),
                            ("MUSICA", "Musica"),
                            ("NARRATIVAS_DIGITALES", "Narrativas Digitales"),
                            ("PSICOLOGIA", "Psicologia"),
                            ("QUIMICA", "Quimica"),
                            ("OTRO", "Otro"),
                        ],
                        default="OTRO",
                        max_length=50,
                    ),
                ),
                ("birthdate", models.DateField()),
                ("friends", models.ManyToManyField(blank=True, to="user.user")),
                ("tags", models.ManyToManyField(blank=True, to="tag.tag")),
            ],
        ),
    ]
