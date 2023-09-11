import pprint
from bisect import bisect_left
import time
import os
import math
import uuid
import random
import regex as re
import numpy as np
import json
import pandas as pd

#django
from randoplant.models import Plant, Region, Size, Affinity
from django.db.models import Sum
from django.db.models.query import QuerySet


pd.set_option('display.max_rows', None)

repeat=0


#MAKE SURE YOU DO NOT PASS A QUERYSET to the plant kwarg

class PlantObject():
	'''all files for resources should be kept here and follow this convention'''
	pd.options.display.max_colwidth = 100
	pd.set_option("display.max_rows", 100)

	_base_dir = os.path.dirname(os.path.abspath(__file__))
	_extremity_file_path = os.path.join(_base_dir, "json", "extremity.json")

	# _sizes_file_path = os.path.join(_base_dir, "json", "size.json")

	@classmethod
	def _read_json(cls, file_name):
		with open(file_name, 'r') as f:
			return json.load(f)

	def __init__(self,plant=None, *args, **kwargs):
		if isinstance(plant, QuerySet):
			raise ValueError("DINGUS: QuerySet type is not allowed for PlantObject(s). Pass in a django model like a real person...")
		self.plant_instance_dataframe_dtypes = {'affinityName':np.str, 'affinityProbability':np.float, 'weightedMarginalAffinity':np.float, 'normalizedAffinity':np.float, 'computedAffinityPotence':np.float, 'affinityRank':np.int}
		self.plant_instance_dataframe_columns = ['affinityName', 'affinityProbability', 'weightedMarginalAffinity', 'normalizedAffinity', 'computedAffinityPotence','affinityRank']
		self.plant_df = None
		self.plant = plant
		self.set_bool = self.plant.continent_origin is not None
		self.region = Region.objects.get(name=self.plant.region.name) if self.set_bool else None
		#self.region = Region.objects.get(name=self.plant.continent_origin) if self.set_bool else None
		self.region_extremity = self.region.extremity
		self.region_base =  self.region.base
		self.region_power =  self.region.power

		# self.base = self.set_base() if self.set_bool else None
		self.extremeness =  self.set_extremeness() if self.set_bool else None
		self.potence =  self.set_potence() if self.set_bool else None

		#extremeness contingent attributes
		self.size =  Size.objects.get(id=self.extremeness) if (self.extremeness is not None) else None
		self.value = self.set_value() if (self.extremeness is not None) else None

		self.affinities = self.generate_instance_biases() if (self.potence is not None) else None
		self.name = f"{self.size.pretty_name} {self.get_dominant_affinity_adjective()} {self.plant.name}"

	def __str__(self):
		return f"{self.size.pretty_name} {self.get_dominant_affinity_adjective()} {self.plant.name}"

	def __repr__(self):
		return f"<< Name:{self.name} - value:({self.value}) potency:({self.potence}) >>"

	def get_dominant_affinity_adjective(self,verbose=False):
		if self.plant_df is None:
			return None
		entry = str(self.plant_df[self.plant_df['finalAffinityPotence'] == self.plant_df['finalAffinityPotence'].max()]['affinityName'].iloc[0])
		affinity_queryset = Affinity.objects.filter(name=entry)
		if affinity_queryset.exists():
			adjective = affinity_queryset.first().adjective
			if verbose:
				print(f'{Affinity.objects.get(name=str(entry)).adjective} {entry}')
			return adjective
		return None

	def set_extremeness(self, modify=False):
		for i in range(1, 14):
			if random.random() > self.region_extremity:
				return i
		return 13

	def set_potence(self,modify=False):
			low = 2 + self.region_base**(self.extremeness-1)
			high = self.region_base**self.extremeness
			n = random.randint(low,high)
			#print(f'rgn_extrem:{self.region_extremity} base:{self.region_base} extr:{self.extremeness} low:{low},high:{high} pot:{n}')
			return n
	def set_value(self, modify=False):
		#this is based upon a lookup of the plant price times the extremeness
		val = (self.potence*self.plant.total_occurence_for_region(str(self.region.name)))**self.extremeness
		return int(str(val)[:15])

	def generate_affinity_probability(self,affinity_percentage):
		return (random.random()*(affinity_percentage/100)) ** self.region_power

	def generate_instance_biases(self, verbose=False):
		biases_dict = {}
		plant_float_fields = self.plant.get_float_fields()
		random.shuffle(plant_float_fields)
		totalAffinityProbability = self.plant.total_affinity_percentage
		potencyTotalAffinityValue = totalAffinityProbability
		cumWeightedAffinityProbability = 0
		plant_df = pd.DataFrame(columns=self.plant_instance_dataframe_columns).astype(self.plant_instance_dataframe_dtypes)
		plant_df['affinityName'] = [field.name for field in plant_float_fields]
		plant_df['affinityProbability'] = [getattr(self.plant, str(field.name)) for field in plant_float_fields]
		plant_df['weightedMarginalAffinity'] = [self.generate_affinity_probability(getattr(self.plant, str(field.name))) for field in plant_float_fields]
		total_marginal_affinity = plant_df['weightedMarginalAffinity'].sum()
		plant_df['normalizedAffinity'] = plant_df['weightedMarginalAffinity'] / total_marginal_affinity
		plant_df['computedAffinityPotence'] = plant_df['normalizedAffinity']*self.potence
		plant_df['finalAffinityPotence'] = round(plant_df['computedAffinityPotence']).astype(int)
		plant_df.sort_values(by='finalAffinityPotence', ascending=True)
		plant_df['affinityRank'] = plant_df['computedAffinityPotence'].rank(method='min', ascending=False).astype(int)
		#assign the raw data to the plant_df attr
		self.plant_df = plant_df.sort_values(by='finalAffinityPotence', ascending=False)
		biases_df = plant_df[plant_df['finalAffinityPotence'] != 0].sort_values(by='finalAffinityPotence', ascending=False)
		for idx, row in biases_df.iterrows():
			biases_dict.setdefault('affinities', {}).update({row['affinityName']:row['finalAffinityPotence']})
		biases_dict['potence'] = self.potence
		biases_dict['name'] = f"{self.size.pretty_name}_{self.get_dominant_affinity_adjective()}_{self.plant.name}".lower()
		biases_dict['price'] = 0
		return biases_dict

		if verbose:pprint.pprint(biases_dict)

	def generate_instance_object(self):
		self.plant_obj

class PlantUtilities:
	def __init__(self,region_bias,random=False,weighted=False):
		#data is probably going to be assigned by inheritance from a game object
		self._data = {"id":"UUID",
		"date_created":"date_timestamp",
		"version":"sample_version",
		"size_string":"descriptive_size_tag",
		"size_val":0,
		"price":0,
		"price_string":"descriptive_price_string"}
		self._plant_bias_obj = self._generate_bias_obj()
		self.plant=None
		self.plant_name = None
		self.regions = {1:'Centriss',2:'Tentacular',3:'Mormiria',4:'Tirelessnight',5:'Reyawinn',0:'Xilewood'}
		self.locaitons=None
		self.region_bias = (region_bias,self.get_region_bias_int(region_bias))
		#self.all_plantnames_in_region=self._plant_bias_obj[self.regions[self.region_bias[1]]]['_dataframe'].iloc[1,:][1:].tolist()
		self._plant_id = "create a unique ID based upon a generated NAME for the plant so I can identify when stuff gets made"
		self.potence = -1
	def get_region_bias_int(self,r):
		return [i for i in self.regions if self.regions[i]==r][0]
	def _sanitize_bias_keystring(self,filepath):
		return re.search(r'.*\_',filepath).group(0)[7:-1].capitalize()
		#this should be a @property
	def _generate_bias_obj(self):
		obj = {}
		#this line is badass because it will always find the file! remember this shit!
		bias_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bias')
		try:
			i = 0
			for file in os.listdir(bias_dir):
				filepath = os.path.join(bias_dir, file)
				sanitized_filepath = self._sanitize_bias_keystring(filepath)
				#THIS NEEDS TO BE CHANGED!
				obj[re.match(r'^.*?(?=_)', file).group(0)] = {
					'_dataframe': pd.read_csv(filepath, encoding='utf-8', delimiter='|')}
				i += 1
		except Exception as e:
			raise ValueError(f'Could not load the biases files - Error:{e}')
		return obj
	def set_plant_attr(self,plant):
		pass
		#anytime the plant getters are run this is run
		#set plant name attr
		#set plant attr
		#set plant columns while on the attr


	#USE THIS TO REBUILD THE DATABASE OF PLANTS!!! (for now)
	def create_plants(self):
		def maker(series,continent):
			p1 = Plant.objects.create(
			name=series[1],
			occurence_value=0,
			common_value=series[0].replace('%', ''),
			metal=series[2].replace('%', ''),
			animal=series[3].replace('%', ''),
			body_control=series[4].replace('%', ''),
			comm_and_emp=series[5].replace('%', ''),
			earth=series[6].replace('%', ''),
			enchantment=series[7].replace('%', ''),
			fire=series[8].replace('%', ''),
			food=series[9].replace('%', ''),
			healing=series[10].replace('%', ''),
			illusion_and_creation=series[11].replace('%', ''),
			knowledge=series[12].replace('%', ''),
			light_and_dark=series[13].replace('%', ''),
			make_and_break=series[14].replace('%', ''),
			meta=series[15].replace('%', ''),
			mind_control=series[16].replace('%', ''),
			movement=series[17].replace('%', ''),
			necromantic=series[18].replace('%', ''),
			plant=series[19].replace('%', ''),
			protection=series[20].replace('%', ''),
			sounds=series[21].replace('%', ''),
			water=series[22].replace('%', ''),
			weather=series[23].replace('%', ''),
			price=series[24].replace('$', ''),
			culinary=series[25].replace('%', ''),
			poison=series[26],
			defense=series[27],
			chemical=series[28],
			symbolic=series[29],
			antidote=series[30],
			continent_origin=Region.objects.filter(name=continent).first())
			p1.save()
		frames = self._plant_bias_obj
		for continent, frame in frames.items():
			print(f'Working on {continent}')
			for col, series in frame['_dataframe'].iteritems():
				if (series[0] == 'Common value'):
					continue
				else:
					print(f'Inserting {series[1]}')
					maker(series,continent)
	def get_plant(self,rgn,col):
		plant = self._plant_bias_obj[self.regions[rgn]]['_dataframe'].iloc[:,[0,col]]
		self.plant=plant
		return plant
	def get_rgn_weighted_plant(self):
		df=self._plant_bias_obj[self.regions[self.region_bias[1]]]['_dataframe']
		options=df.iloc[1].tolist()[1:] #MIGHT NEED TO TAKE THIS OUT
		weights=np.array([i for i in df.iloc[0,:]][1:]).astype(float)
		cdf=np.cumsum(weights/np.sum(weights))
		idx=bisect_left(cdf, np.random.random())
		plant=df.iloc[:,idx]
		self.plant_name=plant[1]
		self.plant=plant
		return plant
	def get_random_plant(self,rgn=None):
		if rgn==None:
			rgn=self.region_bias[1]
		else:
			raise NameError('Need to specify a Region in the class declaration')
		col=random.randint(0,self._plant_bias_obj[self.regions[rgn]]['_dataframe'].shape[1]-1)
		plant=self.get_plant(rgn,col)
		self.plant=plant
		return plant
	def set_plant_state(self,**kwargs):
		#kwarg driven function that sets the state of the class to contain a specific PLANT!
		#also should probably have a setting for removing the heavier memory elements
		#should set a single variable where all of the plant stats are store the whole thing in an object?
		self.plant_name=self.plant['values'][2]
		self._plant_id=self.get_plant_id()
	def get_plant_col(self,rgn=0,col=1,randomize=False,verbose=False):		
		repeat,cnt=True,1
		badnames=['NaN','None',None,"nan","Name"]
		while repeat:
			if randomize:
				plant=self.get_random_plant(rgn)
				plant.columns=['labels', 'values']
				self.plant_name=plant['values'][2]
			else:
				plant=self.get_plant(rgn,col)
				plant.columns=['labels', 'values']
				self.plant_name=plant['values'][2]
			if (self.plant_name not in badnames):
				repeat=False
				break
			else:
				cnt+=1
		return plant
		if (rgn not in self.regions.keys()):
			raise NameError(f'Please enter a valid region: {self.regions}')
	def get_plant_potence(self):
		if self.plant is not None:
			df=self._plant_bias_obj[self.regions[self.region_bias[1]]]['_dataframe']			
			weights=np.array([i for i in df.iloc[0,:]][1:]).astype(float)
			sum_wgt=np.sum(weights)
			#this needs to be set by the region or something...maybe this is manipulated by a character level
			base=10
			extremity=1
			limit=sum_wgt
			#extremity is grabbed from 
			potency=random.randint(2+base**(extremity-1),2+base**extremity)*sum_wgt
			self.potency=potency
	def compute_properties(self):
		pass
	def compute_rarity(self):
		#  https://stackoverflow.com/questions/57217923/what-are-pythonic-methods-for-implementing-random-roll-tables
		#this method is going to make a huge list of tuples that will be massive - around a thousand elements per use. so it needs to be fast - maybe it needs to be a numpy array
		check_bool=(self.plant is not None)
		if check_bool:
			df=self._plant_bias_obj[self.regions[self.region_bias[1]]]['_dataframe']
			occur_range=df.iloc[0][1:].astype(int).sum()
			occur_val=self.plant['values'][0]
			return float(occur_val)/occur_range
			# occurence_prob=self.plant.loc['labels'self.plant_name=

			#here is a row that can be rowsummed to get the occurrence range for the region
			# occur_span=df.iloc[0,:].sum(axis=1)
			# print(occur_span)
def count_elements(seq):
	hist={}
	for i in seq:
		hist[i] = hist.get(i,0)+1
	return hist
def histogram_making():
	
	#test plant maker
	# for i in range(10):
	# 	x.get_plant_col(rgn=1,randomize=True)
	# 	print(f'Plant #{i}...is {x.plant_name}')

	#test rarity

	x.get_plant_col(rgn=1,randomize=True)
	res=[]
	for i in range(1000):
		x.get_rgn_weighted_plant()
		res.append(x.plant_name)
		# print('{}\r'.format(i),end='\r')
	result_dic=count_elements(res)
	_dic=((value,key) for (key,value) in result_dic.items())
	s=sorted(_dic,reverse=True)
	pprint.pprint(s)

def checkit():
	x = PlantUtilities('Centriss')
	x.get_random_plant()
	x.get_plant_potence()
	# test the function sometime and make sure its a histogram


if __name__ =="__main__":
	checkit()

