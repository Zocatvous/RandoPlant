import pprint
from bisect import bisect_left
import os
import math
import uuid
import random
import regex as re
import numpy as np
import json
import pandas as pd

#django
from randoplant.models import Plant
from django.db.models import Sum

pd.set_option('display.max_rows', None)
#All we want to do for the moment is make a class that looks up the "string" of the regional bias and loads the biases as a datafram to a dataframe object in an attribute. 

'''
underscored properties and attributes are "meta" sort of things that help drive the object functionally
non-underscored methods and attributes are for setting the plant
eventually there will be differentiation between GET and SET functions that will either set attributes or retrieve values as an output
but we are doing both at once for the time being


Class kwargs are 
- a currently mandatory regional bias flag
- a random flag for true random behavior
- a wieghted mode for what will be used to generate all flowers according to region

F59 should be a variable called "base"
E60 should be a variable called "extremity" calculated like this
Heres a function that needs to generate an integer that fits the specified criteria

=randbetween(2+F59^(E60-1),F59^E60)

F59 should be a variable called "base"
E60 should be a variable called "extremity" calculated like this

'''
repeat=0
class PlantObject(Plant):
	'''all files for resources should be kept here and follow this convention'''
	base_dir = os.path.dirname(os.path.abspath(__file__))
	extremity_file_path = os.path.join(base_dir, "json", "extremity.json")
	
	@classmethod
	def _read_json_file(cls, file_name):
		with open(file_name, 'r') as f:
			return json.load(f)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.extremity_dict = PlantObject._read_json_file(PlantObject.extremity_file_path)
		self.sizes = []
		self.base = 10
		self.region = self.get_region()
		self.potence = self.get_potence()
		self.extremity = self.get_extremity(region)

	def get_region_extremity(self, region, modify=False):
		return self.extremity_dict[region]['extremity']

	def get_region_base(self,region,modify=False):
		return self.extremity_dict[region]['base']

	def get_region_power(self,region, modify=False):
		return self.extremity_dict[region]['power']

	def get_potence(self, region, modify=False):
		potence = random.randint(2+)

	def get_price(self):
		pass

#this is the master setter for all plant instance attributes - this will likely need a TON of 
	def set_plant_object_instance(self, region):
		r = random.random()		
		plant = self.select_plant_by_region(region)
		extremity = self.get_region_extremity(region)
		potence = self.get_potence()
		ex_val =  next((i for i in range(1, 14) if random.random() > extremity), 1)

#this method interfaces with the database and selects a plant template based upon region, randomness-type, and crazy value
	@classmethod
	def select_plant_by_region(self, region, crazy_value=False, true_random=False):
		plants = Plant.objects.filter(continent_origin=region)
		if not true_random:
			total_occurence_value = plants.aggregate(Sum('common_value'))['common_value__sum']
			cdf = []
			cumulative_value = 0
			for plant in plants:
				cumulative_value += plant.common_value
				cdf.append((cumulative_value + crazy_value - 0.000001) / total_occurence_value)
			random_value = random.random() if not crazy_value else random.uniform(0.89, 0.99)
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




class PlantUtilities:
	def __init__(self,regional_bias,random=False,weighted=False):
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
		self.regional_bias = (regional_bias,self.get_regional_bias_int(regional_bias))
		#self.all_plantnames_in_region=self._plant_bias_obj[self.regions[self.regional_bias[1]]]['_dataframe'].iloc[1,:][1:].tolist()
		self._plant_id = "create a unique ID based upon a generated NAME for the plant so I can identify when stuff gets made"
		self.potence = -1
	def get_regional_bias_int(self,r):
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
		
	#property
	def get_plant_power_profile(self):
		pass
	def get_plant_price(self):
		pass
	def get_plant(self,rgn,col):
		plant = self._plant_bias_obj[self.regions[rgn]]['_dataframe'].iloc[:,[0,col]]
		self.plant=plant
		return plant
	def get_rgn_weighted_plant(self):
		df=self._plant_bias_obj[self.regions[self.regional_bias[1]]]['_dataframe']
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
			rgn=self.regional_bias[1]
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
			df=self._plant_bias_obj[self.regions[self.regional_bias[1]]]['_dataframe']			
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
			df=self._plant_bias_obj[self.regions[self.regional_bias[1]]]['_dataframe']
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

