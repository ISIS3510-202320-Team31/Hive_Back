# Generated by Django 4.2 on 2023-11-30 02:34

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        ('link', '0001_initial'),
        ('tag', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image', models.CharField(max_length=500)),
                ('name', models.CharField(max_length=50)),
                ('place', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('description', models.CharField(max_length=500)),
                ('num_participants', models.IntegerField(null=True)),
                ('category', models.CharField(choices=[('ACADEMIC', 'Academic'), ('CULTURAL', 'Cultural'), ('SPORTS', 'Sports'), ('ENTERTAINMENT', 'Entertainment'), ('OTHER', 'Other')], default='OTHER', max_length=20)),
                ('state', models.BooleanField(default=True)),
                ('duration', models.IntegerField(null=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
                ('links', models.ManyToManyField(related_name='links', to='link.link')),
                ('participants', models.ManyToManyField(related_name='participants', to='user.user')),
                ('tags', models.ManyToManyField(related_name='tags', to='tag.tag')),
            ],
        ),
    ]
