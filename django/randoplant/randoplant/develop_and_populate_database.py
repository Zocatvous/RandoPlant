from randoplant.plant import PlantUtilities
from randoplant.modles import Plant
x = PlantUtilities('Centriss')
frames = x._plant_bias_obj
index = None
for k,v in frames.items():
	for col, series in v['_dataframe'].iteritems():
		if (series[0] == 'Common value'):
			print(True)
			index = series
		else:
			input(series)
			input(f'the {series[3]} value for {} is {}')
