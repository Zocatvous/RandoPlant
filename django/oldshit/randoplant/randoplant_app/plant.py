import pprint
from bisect import bisect_left
import os
import math
import uuid
import random
import regex as re
import numpy as np
import pandas as pd
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
-

'''
repeat=0
class Plant:
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
		self.all_plantnames_in_region=self._plant_bias_obj[self.regions[self.regional_bias[1]]]['_dataframe'].iloc[1,:][1:].tolist()
		self._plant_id = "create a unique ID based upon a generated NAME for the plant so I can identify when stuff gets made"
		self.potence = -1
	def get_regional_bias_int(self,r):
		return [i for i in self.regions if self.regions[i]==r][0]
	def _sanitize_bias_keystring(self,filepath):
		return re.search(r'.*\_',filepath).group(0)[7:-1].capitalize()
		#this should be a @property
	def _generate_bias_obj(self):
		obj = {}
		bias_dir = r'./bias/'
		try:
			i = 0
			for file in os.listdir(bias_dir):
				filepath = os.path.join(bias_dir, file)
				sanitized_filepath = self._sanitize_bias_keystring(filepath)
				obj[sanitized_filepath] = {
					'_name': sanitized_filepath,
					'id': i,
					'_filestring': filepath,
					'_dataframe': pd.read_csv(filepath, encoding='utf-8', delimiter='|'),
					'base':None}
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
	x = Plant('Centriss')
	x.get_random_plant()
	x.get_plant_potence()
	# test the function sometime and make sure its a histogram


if __name__ =="__main__":
	checkit()

