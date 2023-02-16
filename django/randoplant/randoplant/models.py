from django.db import models
from django.db.models import Sum
from random import random, uniform

# class GameObject(models.Model):
# 	game_object_id=models.IntegerField(null=False, db_index=True, on_delete=models.CASCADE)
# 	name=models.CharField(max_length=100)
# 	object_type=OneToManyField(Plant)

class Plant(models.Model):
	#game_object_id=models.ForeignKey(GameObject, related_name="plant", on_delete=models.CASCADE)
	name=models.TextField(max_length=50,null=False, blank=True)
	occurence_value=models.IntegerField(null=True, default=0)
	common_value=models.IntegerField(null=True, default=0)
	#continent=models.ForiegnKey(Continent, related_name="plant",max_length=30)
	metal=models.FloatField(default=0.0,null=False,blank=True)
	animal=models.FloatField(default=0.0,null=False,blank=True)
	body_control=models.FloatField(default=0.0,null=False,blank=True)
	comm_and_emp=models.FloatField(default=0.0,null=False,blank=True)
	earth=models.FloatField(default=0.0,null=False,blank=True)
	enchantment=models.FloatField(default=0.0,null=False,blank=True)
	fire =models.FloatField(default=0.0,null=False,blank=True)
	food=models.FloatField(default=0.0,null=False,blank=True)
	healing=models.FloatField(default=0.0,null=False,blank=True)
	illusion_and_creation=models.FloatField(default=0.0,null=False,blank=True)
	knowledge=models.FloatField(default=0.0,null=False,blank=True)
	light_and_dark=models.FloatField(default=0.0,null=False,blank=True)
	make_and_break=models.FloatField(default=0.0,null=False,blank=True)
	meta=models.FloatField(default=0.0,null=False,blank=True)
	mind_control=models.FloatField(default=0.0,null=False,blank=True)
	movement=models.FloatField(default=0.0,null=False,blank=True)
	necromantic=models.FloatField(default=0.0,null=False,blank=True)
	plant=models.FloatField(default=0.0,null=False,blank=True)
	protection=models.FloatField(default=0.0,null=False,blank=True)
	sounds=models.FloatField(default=0.0,null=False,blank=True)
	water=models.FloatField(default=0.0,null=False,blank=True)
	weather=models.FloatField(default=0.0,null=False,blank=True)
	price=models.FloatField(default=0.0,null=True,blank=True)
	culinary=models.CharField(max_length=50, default=None,null=True,blank=True)
	poison=models.CharField(max_length=50, default=None,null=True,blank=True)
	defense=models.TextField(default=None,null=True,blank=True)
	chemical=models.CharField(default=0.0,null=True,blank=True,max_length=200)
	symbolic=models.TextField(default=0.0,null=True,blank=True,max_length=200)
	antidote=models.CharField(default=0.0,null=True,blank=True,max_length=200)
	continent_origin=models.CharField(max_length=30,null=False,blank=True)
	description=models.TextField(default=None,max_length=300, null=True, blank=True)

	def __str__(self):
		return f"<{self.name} - Commonality:{self.common_value}/{self.total_occurence_for_region(self.continent_origin)}>"

	def get_highest_plant_affinity(self):
		pass

	@property
	def region(self):
		return self.continent_origin

	@property
	def rarity(self):
		rarity = ((self.common_value / self.total_occurence_for_region(self.continent_origin)))
		return round(rarity, 4)
	
	def total_occurence_for_region(self, region):
		plants = Plant.objects.filter(continent_origin=region)
		total_occurence_value = plants.aggregate(Sum('common_value'))['common_value__sum']
		return total_occurence_value

	@classmethod
	def select_plant_by_region(self, region, crazy_value=False, true_random=False, true_region=False):
		plants = Plant.objects.filter(continent_origin=region)
		if not true_random:
			total_occurence_value = plants.aggregate(Sum('common_value'))['common_value__sum']
			cdf = []
			cumulative_value = 0
			for plant in plants:
				cumulative_value += plant.common_value
				cdf.append((cumulative_value + crazy_value - 0.000001) / total_occurence_value)
			random_value = random() if not crazy_value else uniform(0.89, 0.99)
			for i, value in enumerate(cdf):
				if random_value <= value:
					return plants[i]
		else:
			return random.choice(plants)
		return None

class Events(models.Model):
	name=models.TextField(max_length=50,null=False, blank=True)
	continent_origin=models.CharField(max_length=30,null=False,blank=True)
	description=models.TextField(default=None,max_length=300, null=True, blank=True)
	text=models.TextField(default=None,max_length=300, null=True, blank=True)

class Compound(models.Model):
	name=models.TextField(max_length=50,null=False, blank=True)



#eventually make this a foreign key to the Plant model and remove all the regional lookup crap from the PlantINstance
class Region(models.Model):
	name=models.TextField(max_length=50,null=False)
	# def clean(self):
		


# class Continent(models.GameObject):
# 	game_object_id-models.ForiegnKey(GameObject, related_name='continent', on_delete=models.CASCADE)
# 	continent_id=models.IntegerKey(null=False,blank=True)
# 	name=models.CharField(max_length=30)

# class Item(models.GameObject):
# 	game_object_id=models.IntegerField()
# 	name=models.CharField(max_length=50)

