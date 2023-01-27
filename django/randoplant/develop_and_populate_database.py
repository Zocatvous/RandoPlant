import os
import django_extensions
from randoplant.plant import PlantUtilities
from randoplant.models import Plant
from django.conf import settings
import re

def extract_substring(string):
    match = re.search(r'/bias/(.*?)_bias', string)
    if match:
        return match.group(1)
    else:
        return None

#settings.configure()
x = PlantUtilities('Centriss')
frames = x._plant_bias_obj
index = None
input(frames)
for k,v in frames.items():
	if (k == '_dataframe'):
		print(
			f"looping over the \
			{extract_substring(v['_filestring'])}\
			 dict with {len(v['_dataframe'])} \
			  elem.")
		input()	
		for col, series in v['_dataframe'].iteritems():
			if (series[0] == 'Common value'):
				pass
			else:
				print(f'...inserting {series[1]}')
				Plant.objects.create(
				name=series[1],
				occurence_value=0,
				common_value=series[0].replace('%',''),
				metal=series[2].replace('%',''),
				animal=series[3].replace('%',''),
				body_control=series[4].replace('%',''),
				comm_and_emp=series[5].replace('%',''),
				earth=series[6].replace('%',''),
				enchantment=series[7].replace('%',''),
				fire=series[8].replace('%',''),
				food=series[9].replace('%',''),
				healing=series[10].replace('%',''),
				illusion_and_creation=series[11].replace('%',''),
				knowledge=series[12].replace('%',''),
				light_and_dark=series[13].replace('%',''),
				make_and_break=series[14].replace('%',''),
				meta=series[15].replace('%',''),
				mind_control=series[16].replace('%',''),
				movement=series[17].replace('%',''),
				necromantic=series[18].replace('%',''),
				plant=series[19].replace('%',''),
				protection=series[20].replace('%',''),
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
				continent_origin=extract_substring(v['_filestring'])

