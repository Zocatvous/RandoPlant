# Generated by Django 4.1.5 on 2023-02-17 09:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('randoplant', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='size',
            name='lookup_id',
        ),
    ]
