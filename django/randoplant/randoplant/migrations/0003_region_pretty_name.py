# Generated by Django 4.1.5 on 2023-02-17 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('randoplant', '0002_remove_size_lookup_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='region',
            name='pretty_name',
            field=models.TextField(max_length=20, null=True),
        ),
    ]