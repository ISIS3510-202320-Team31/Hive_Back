# Generated by Django 4.2 on 2023-10-02 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0006_alter_event_description_alter_event_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.CharField(max_length=500),
        ),
    ]