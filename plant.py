import pprint
import os
import math
import uuid
import random
import regex as re
import pandas as pd
pd.set_option('display.max_rows', None)
#All we want to do for the moment is make a class that looks up the "string" of the regional bias and loads the biases as a datafram to a dataframe object in an attribute. 

'''
underscored properties and attributes are "meta" sort of things that help drive the object functionally
non-underscored methods and attributes are for setting the plant
'''
repeat=0
class Plant:
	def __init__(self,regional_bias):
		self._data = {"id":"UUID",
		"date_created":"date_timestamp",
		"version":"sample_version",
		"size_string":"descriptive_size_tag",
		"size_val":0,
		"price":0,
		"price_string":"descriptive_price_string"}
		self._plant_bias_obj = self._generate_bias_obj()
		print()
		self.plant=None
		self.plant_name = None
		self.regions = {1:'Centriss',2:'Tentacular',3:'Mormiria',4:'Tirelessnight',5:'Reyawinn',0:'Xilewood'}
		self.regional_bias = regional_bias
		self.region = "sample_region_name"
		self._region_bias = regional_bias
		self._plant_id = "create a unique ID based upon a generated NAME for the plant so I can identify when stuff gets made"
		self.potence = -1
	def _sanitize_bias_keystring(self,filepath):
		return re.search(r'.*\_',filepath).group(0)[7:-1].capitalize()
	def _generate_bias_obj(self):
		
		obj={}
		bias_dir=r'./bias/'
		try:
			i=0
			for file in os.listdir(bias_dir):
				filepath = os.path.join(bias_dir,file)
				obj[self._sanitize_bias_keystring(filepath)] = {'_name':self._sanitize_bias_keystring(filepath),'id':i,f'_filestring':filepath,'_dataframe':pd.read_csv(filepath, encoding='utf-8',delimiter='|')}
				i+=1
		except Exception as e:
			raise ValueError(f'Could not load the biases files - Error:{e}')
		return obj
	def get_plant_power_profile(self):
		pass
	def get_plant_price(self):
		pass
	def get_plant(self,rgn,col):
		return self._plant_bias_obj[self.regions[rgn]]['_dataframe'].iloc[:,[0,col]]
	def get_random_plant(self,rgn):
		col=random.randint(0,self._plant_bias_obj[self.regions[rgn]]['_dataframe'].shape[1]-1)
		plant=self.get_plant(rgn,col)
		# self.plant_name=plant['values'][2]
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
	def compute_properties(self):
		pass

	def compute_rarity(self):
		#there is a row that can be rowsummed to get the occurrence range for the region
		span=0
	


def checkit():
	x = Plant('Cenriss')
	for i in range(10):
		x.get_plant_col(rgn=1,randomize=True)
		print(f'Plant #{i}...is {x.plant_name}')

if __name__ =="__main__":
	checkit()

