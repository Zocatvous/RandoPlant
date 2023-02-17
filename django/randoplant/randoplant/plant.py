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
from randoplant.models import Plant, Region, Size
from django.db.models import Sum

pd.set_option('display.max_rows', None)
#All we want to do for the moment is make a class that looks up the "string" of the region bias and loads the biases as a datafram to a dataframe object in an attribute. 

'''
underscored properties and attributes are "meta" sort of things that help drive the object functionally
non-underscored methods and attributes are for setting the plant
eventually there will be differentiation between GET and SET functions that will either set attributes or retrieve values as an output
but we are doing both at once for the time being


Class kwargs are 
- a currently mandatory region bias flag
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
class PlantObject():
	'''all files for resources should be kept here and follow this convention'''
	_base_dir = os.path.dirname(os.path.abspath(__file__))
	_extremity_file_path = os.path.join(_base_dir, "json", "extremity.json")
	# _sizes_file_path = os.path.join(_base_dir, "json", "size.json")

	@classmethod
	def _read_json(cls, file_name):
		with open(file_name, 'r') as f:
			return json.load(f)

	def __init__(self,plant=None, *args, **kwargs):
		self.plant = plant
		self.set_bool = (self.plant.continent_origin is not None)
		self.region = Region.objects.filter(plant__name=self.plant.name) if self.set_bool else None
		self.region_extremity = Region.objects.get(name=self.plant.continent_origin).extremity
		self.region_base =  Region.objects.get(name=self.plant.continent_origin).base
		self.region_power =  Region.objects.get(name=self.plant.continent_origin).power

		# self.base = self.set_base() if self.set_bool else None
		self.extremeness =  self.set_extremeness() if self.set_bool else None
		self.potence =  self.set_potence() if self.set_bool else None

		#extremeness contingent attributes
		self.size =  Size.objects.get(self.extremeness) if (self.extremeness is not None) else None
		self.value = self.set_value() if (self.extremeness is not None) else None

	# def get_region_extremity(self, modify=False):
	# 	return self.extremity_dict[self.instance_region]['extremity']
	# def get_region_base(self,modify=False):
	# 	return self.extremity_dict[self.instance_region]['base']
	# def get_region_power(self, modify=False):
	# 	return self.extremity_dict[self.instance_region]['power']
	def set_extremeness(self, modify=False):
		for i in range(1, 14):
			if random.random() > self.region_extremity:
				return i
		return 13
	def set_potence(self,modify=False):
			low = 2 + self.region_base**(self.extremeness-1)
			high = self.region_base**self.extremeness
			return random.randint(low,high)

	def set_value(self, modify=False):
		#this is based upon a lookup of the plant price times the extremeness 
		return self.extremeness*self.plant.total_occurence_for_region(str(self.instance_region))


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
		
	#property
	def get_plant_power_profile(self):
		pass
	def get_plant_price(self):
		pass

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

