import os
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "randoplant.settings")
import django_extensions

from plant import PlantUtilities
from models import Plant
from django.conf import settings
#settings.configure()
x = PlantUtilities('Centriss')
frames = x._plant_bias_obj
index = None
for k,v in frames.items():
	for col, series in v['_dataframe'].iteritems():
		if (series[0] == 'Common value'):
			print(True)
			index = series
		input(f'the {index[3]} is {series[3]} and the series Body Control value is {series[5]}')
