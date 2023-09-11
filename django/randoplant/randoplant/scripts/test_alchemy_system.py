
from randoplant.models import Affinity, CharacterSheet, Compound, Effect, Events, Plant, Region, Size, Tool
import random, pprint
from randoplant.plant import PlantObject
#_object = PlantObject(plant=Plant.objects.filter(name='Wheat'))
#test = Affinity.objects.get(name=str(PlantObject.get_dominant_affinity_adjective())) if (self.affinities is not None) else None


# plant_objects_list = []
# random_plants = Plant.objects.order_by('?')[0:4]
# for p in random_plants:
# 	plant_obj = PlantObject(plant=p)
# 	pprint.pprint(p.affinities)
# 	plant_objects_list.append(plant_obj)
wheat = PlantObject(plant=Plant.objects.filter(name='Wheat').first())
clericalus = PlantObject(plant=Plant.objects.filter(name='Clericalus').first())
carrot = PlantObject(plant=Plant.objects.filter(name='Carrot').first())


wheat = PlantObject(plant=Plant.objects.filter(name='Wheat').first())
clericalus = PlantObject(plant=Plant.objects.filter(name='Clericalus').first())
carrot = PlantObject(plant=Plant.objects.filter(name='Carrot').first())
random_plants = [wheat,clericalus,carrot]
#for plant in random_plants:
	#print(plant.name)
	#print(plant.affinities)



# now I need to add all of the "names" of all the plants used to combine and create the affinity stack objects 

def stack_affinities(*plant_objects):
	plant_list = list(plant_objects)
	print(plant_list)
	first_plant = plant_list.pop(0)
	combined_affinities = first_plant

	print(f'first plant:{first_plant}')
	print(f'affinities: {first_plant.affinities}')
	for p in plant_list:
		print(f'iterating on {p}')
		combined_affinities.affinities['potence'] += p.affinities['potence'] 
		for key, value in p.affinities['affinities'].items():
			if isinstance(value, str):
				print('found the name key skipping')
				continue
			elif key in first_plant.affinities['affinities'].keys():
				print(f'first_plant has {key}')
				combined_affinities.affinities['affinities'][key]+=value
			else:
				print(f'first_plant doesnt have {key} ... adding')
				combined_affinities.affinities['affinities'][key] = value
	return {'combined_affinities':combined_affinities.affinities}


# wheat = PlantObject(plant=Plant.objects.filter(name='Wheat').first())
# clericalus = PlantObject(plant=Plant.objects.filter(name='Clericalus').first())
# carrot = PlantObject(plant=Plant.objects.filter(name='Carrot').first())


#x=stack_affinities(wheat, carrot, clericalus)
#pprint.pprint(x)


# I Might need to remake t