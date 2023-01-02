from django.db import models


class GameObject(models.Model):
	id=models.IntegerField()
	name=models.CharField(max_length=100)
	type=

class Plant(GameObject):
	instance_id=models.IntegerField()
	name=models.CharField(max_length=50)

class Item(GameObject):
	instance_id=models.IntegerField()
	name=models.CharField(max_length=50)

