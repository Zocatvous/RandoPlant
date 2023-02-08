import os
from django_extensions 
from randoplant.plant import PlantUtilities
from randoplant.models import Plant
from django.conf import settings
from django.apps import apps
import re

# import sys
# sys.path.append('/home/zoctavous/vault/repos/misc/RandoPlant/django/randoplant/runscript')
# from djago_extensions.runscript import develop



def extract_substring(string):
    match = re.search(r'/bias/(.*?)_bias', string)
    if match:
        return match.group(1)
    else:
        return None


def creater(series,k):
	Plant.objects.create(
				name=series[1], \
				occurence_value=0, \
				common_value=series[0].replace('%',''), \
				metal=series[2].replace('%',''), \
				animal=series[3].replace('%',''), \
				body_control=series[4].replace('%',''), \
				comm_and_emp=series[5].replace('%',''), \
				earth=series[6].replace('%',''), \
				enchantment=series[7].replace('%',''), \
				fire=series[8].replace('%',''), \
				food=series[9].replace('%',''), \
				healing=series[10].replace('%',''), \
				illusion_and_creation=series[11].replace('%',''), \
				knowledge=series[12].replace('%',''), \
				light_and_dark=series[13].replace('%',''), \
				make_and_break=series[14].replace('%',''), \
				meta=series[15].replace('%',''), \
				mind_control=series[16].replace('%',''), \
				movement=series[17].replace('%',''), \
				necromantic=series[18].replace('%',''), \
				plant=series[19].replace('%',''), \
				protection=series[20].replace('%',''), \
				sounds=series[21].replace('%',''), \
				water=series[22].replace('%',''), \
				weather=series[23].replace('%',''), \
				price=series[24].replace('$',''), \
				culinary=series[25].replace('%',''), \
				poison=series[26], \
				defense=series[27], \
				chemical=series[28], \
				symbolic=series[29], \
				antidote=series[30], \
				continent_origin=k)


x = PlantUtilities('Centriss')
frames = x._plant_bias_obj
for k,v in frames.items():
	print(f'...Working on ({k})')
	for col, series in x._plant_bias_obj[k]['_dataframe'].iteritems():
		if (series[0] == 'Common value'):
			pass
		else:
			print(f'...inserting {series[1]}')
			creater(series,k)
		# for p in Plant.objects.all():print(f'{p.name} - {p.continent_origin}')
			input('check?')
Plant.save()

x = PlantUtilities('Centriss')
	frames = x._plant_bias_obj
	for k,v in frames.items():
		print(f'...Working on ({k})')
		for col, series in x._plant_bias_obj[k]['_dataframe'].iteritems():
			if (series[0] == 'Common value'):
				pass
			else:
				print(f'...inserting {series[1]}')
				Plant.objects.create(name=series[1],occurence_value=0,common_value=series[0].replace('%',''),metal=series[2].replace('%',''),animal=series[3].replace('%',''),body_control=series[4].replace('%',''),comm_and_emp=series[5].replace('%',''),earth=series[6].replace('%',''),enchantment=series[7].replace('%',''),fire=series[8].replace('%',''),food=series[9].replace('%',''),healing=series[10].replace('%',''),illusion_and_creation=series[11].replace('%',''),knowledge=series[12].replace('%',''),light_and_dark=series[13].replace('%',''),make_and_break=series[14].replace('%',''),meta=series[15].replace('%',''),mind_control=series[16].replace('%',''),movement=series[17].replace('%',''),necromantic=series[18].replace('%',''),plant=series[19].replace('%',''),protection=series[20].replace('%',''),
				sounds=series[21].replace('%',''),
				water=series[22].replace('%',''),
				weather=series[23].replace('%',''),
				price=series[24].replace('$',''),
				culinary=series[25].replace('%',''),
				poison=series[26],
				defense=series[27],
				chemical=series[28],
				symbolic=series[29],
				antidote=series[30],
				continent_origin=k)
				input('check?')
