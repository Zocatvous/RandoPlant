# Generated by Django 4.1.5 on 2023-02-10 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('randoplant', '0003_alter_plant_defense'),
    ]

    operations = [
        migrations.AddField(
            model_name='plant',
            name='description',
            field=models.TextField(blank=True, default=None, max_length=300, null=True),
        ),
    ]
