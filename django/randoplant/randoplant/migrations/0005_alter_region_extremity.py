# Generated by Django 4.1.5 on 2023-02-28 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('randoplant', '0004_affinity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='region',
            name='extremity',
            field=models.FloatField(default=0, null=True),
        ),
    ]
