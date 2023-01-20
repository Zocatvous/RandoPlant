from django.db import models


# class GameObject(models.Model):
# 	game_object_id=models.IntegerField(null=False, db_index=True, on_delete=models.CASCADE)
# 	name=models.CharField(max_length=100)
# 	object_type=OneToManyField(Plant)

class Plant(models.Model):
	#game_object_id=models.ForeignKey(GameObject, related_name="plant", on_delete=models.CASCADE)
	name=models.TextField(max_length=50, blank=True)
	occurence_value=models.IntegerField(null=True, default=0)
	common_value=models.IntegerField(null=True, default=0)
	#continent=models.ForiegnKey(Continent, related_name="plant",max_length=30)
	metal=models.FloatField(default=0.0,null=False,blank=False)
	animal=models.FloatField(default=0.0,null=False,blank=False)
	body_control=models.FloatField(default=0.0,null=False,blank=False)
	comm_and_emp=models.FloatField(default=0.0,null=False,blank=False)
	earth=models.FloatField(default=0.0,null=False,blank=False)
	enchantment=models.FloatField(default=0.0,null=False,blank=False)
	fire =models.FloatField(default=0.0,null=False,blank=False)
	food=models.FloatField(default=0.0,null=False,blank=False)
	healing=models.FloatField(default=0.0,null=False,blank=False)
	illusion_and_creation=models.FloatField(default=0.0,null=False,blank=False)
	knowledge=models.FloatField(default=0.0,null=False,blank=False)
	light_and_dark=models.FloatField(default=0.0,null=False,blank=False)
	make_and_break=models.FloatField(default=0.0,null=False,blank=False)
	meta=models.FloatField(default=0.0,null=False,blank=False)
	mind_control=models.FloatField(default=0.0,null=False,blank=False)
	movement=models.FloatField(default=0.0,null=False,blank=False)
	necromantic=models.FloatField(default=0.0,null=False,blank=False)
	plant=models.FloatField(default=0.0,null=False,blank=False)
	protection=models.FloatField(default=0.0,null=False,blank=False)
	sounds=models.FloatField(default=0.0,null=False,blank=False)
	water=models.FloatField(default=0.0,null=False,blank=False)
	weather=models.FloatField(default=0.0,null=False,blank=False)
	price=models.FloatField(default=0.0,null=False,blank=False)
	culinary=models.FloatField(default=0.0,null=False,blank=False)
	poison=models.FloatField(default=0.0,null=False,blank=False)
	defense=models.FloatField(default=0.0,null=False,blank=False)
	chemical=models.FloatField(default=0.0,null=False,blank=False)
	symbolic=models.FloatField(default=0.0,null=False,blank=False)
	antidote=models.FloatField(default=0.0,null=False,blank=False)
	continent_origin=models.CharField(max_length=30,null=False,blank=False)

	def __str__(self):
		return f"{self.name} - {self.common_value} - Some other things"


# class Continent(models.GameObject):
# 	game_object_id-models.ForiegnKey(GameObject, related_name='continent', on_delete=models.CASCADE)
# 	continent_id=models.IntegerKey(null=False,blank=False)
# 	name=models.CharField(max_length=30)

# class Item(models.GameObject):
# 	game_object_id=models.IntegerField()
# 	name=models.CharField(max_length=50)

