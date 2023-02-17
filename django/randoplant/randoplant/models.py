from django.db import models
from django.db.models import Sum
from django.contrib.postgres.fields import ArrayField

from random import random, uniform

# class GameObject(models.Model):
# 	game_object_id=models.IntegerField(null=False, db_index=True, on_delete=models.CASCADE)
# 	name=models.CharField(max_length=100)
# 	object_type=OneToManyField(Plant)



#eventually make this a foreign key to the Plant model and remove all the regional lookup crap from the PlantINstance
class Region(models.Model):
	name = models.TextField(max_length=50, null=False)
	base = models.IntegerField(default=0, null=True)
	extremity = models.IntegerField(default=0, null=True)
	power = models.IntegerField(default=0, null=True)
	pretty_name = models.TextField(max_length=20, null=True)
	# nissia_region_affinity = models.FloatField(default=0.0)
	# thewhip_region_affinity = models.FloatField(default=0.0)
	# kellarn_region_affinity = models.FloatField(default=0.0)
	# centriss_region_affinity = models.FloatField(default=0.0)
	# essianfoothills_region_affinity = models.FloatField(default=0.0)
	# shipyards_region_affinity = models.FloatField(default=0.0)
	# firstcity_region_affinity = models.FloatField(default=0.0)
	# xilewood_region_affinity = models.FloatField(default=0.0)
	# emmel_region_affinity = models.FloatField(default=0.0)
	# tirelessnight_region_affinity = models.FloatField(default=0.0)
	# tentacular_region_affinity = models.FloatField(default=0.0)
	# wanderlands_region_affinity = models.FloatField(default=0.0)
	# ostentia_region_affinity = models.FloatField(default=0.0)
	# hub_region_affinity = models.FloatField(default=0.0)
	# worldspine_region_affinity = models.FloatField(default=0.0)
	# sinisteria_region_affinity = models.FloatField(default=0.0)
	# riddlewood_region_affinity = models.FloatField(default=0.0)
	# lostpeaks_region_affinity = models.FloatField(default=0.0)
	# mormiria_region_affinity = models.FloatField(default=0.0)
	# reyawinn_region_affinity = models.FloatField(default=0.0)
	def __str__(self):
		return f"{self.pretty_name}"

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
	continent_origin = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='plants')
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


	@classmethod
	def total_occurence_for_region(cls, region):
		if isinstance(region, str):
			region_name = region
		elif isinstance(region, Region):
			region_name = region.name
		else:
			raise TypeError(f"Invalid region type: {type(region)}")

		plants = Region.objects.get(name=region_name.lower().replace(' ','')).plants.all()
		total_occurence_value = plants.aggregate(Sum('common_value'))['common_value__sum']
		return total_occurence_value

	@classmethod
	def select_plant_by_region(self, region, crazy_value=False, true_random=False, true_region=False):
		plants = Region.objects.get(name=region).plants.all()
		# plants = p_region.plants.all()
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

	@classmethod	
	def _test_profile_weighted_plants_in_region(self,count=100,region='centriss',run_all_regions=False):
		flower_count = {}
		for i in range(count):
			print('picking {} flowers...\r'.format(i),end='\r')
			flower = self.select_plant_by_region(region)
			if flower.name not in flower_count:
				flower_count[flower.name] = 0
			flower_count[flower.name] += 1
		pprint.pprint(flower_count)
		return flower_count

class Size(models.Model):
	name=models.TextField(max_length=50,null=False)
	pretty_name=models.TextField(max_length=25,null=False)

	def __str__(self):
		return f"{self.pretty_name} - ({self.id})"

class Events(models.Model):
	name=models.TextField(max_length=50,null=False, blank=True)
	continent_origin=models.CharField(max_length=30,null=False,blank=True)
	description=models.TextField(default=None,max_length=300, null=True, blank=True)
	text=models.TextField(default=None,max_length=300, null=True, blank=True)

class Compound(models.Model):
	name=models.TextField(max_length=50,null=False, blank=True)
	# ingredients=ArrayField(models.CharField(max_length=50), default=list)

class Affinities(models.Model):
	name=CharField(max_length=30,null=True)
	adjective=CharField(max_length=30,null=True)

# class Continent(models.GameObject):
# 	game_object_id-models.ForiegnKey(GameObject, related_name='continent', on_delete=models.CASCADE)
# 	continent_id=models.IntegerKey(null=False,blank=True)
# 	name=models.CharField(max_length=30)

# class Item(models.GameObject):
# 	game_object_id=models.IntegerField()
# 	name=models.CharField(max_length=50)

