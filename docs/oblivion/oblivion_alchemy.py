import pandas as pd
import pprint
pd.set_option('display.max_rows',500)

def construct_all_ingredients_df(path_to_ingredients):
	ing_df = pd.read_csv(path_to_ingredients)
	for col in ing_df.columns:
		ing_df[col] = ing_df[col].apply(lambda x: str(x).lower().replace(" ", "_"))
	print(ing_df)
	return ing_df




# I NEED TO RETHINK HOW I AM HANDLING the instrument strength there needs to be a function that maps "strength"

# Quality	Strength
# Novice	0.1
# Apprentice	0.25
# Journeyman	0.5
# Expert	0.75
# Master	1

# from a quality string and from a number

class AlchemyFactory:
	def __init__(self, alembic_level='novice', calcinator_level='novice',pestlemortar_level='novice', retort_level='novice', luck_level=20, alchemy_level=1):
		print('- Oblivion Alchemy in Python -')
		self.al = 1
		self.ingredients = construct_all_ingredients_df('./processed_flower_effects.csv')
		#lists
		self.duration_only_effects_list = []
		self.magnitude_only_effects_list = []
		self.negative_effects_list = []
		self.positive_effects_list = []
		#constants- may need something else for this to refresh state on things
		self.effective_alchemy_level = alchemy_level+0.4*(luck_level-50)

	def get_unique_effects(self):
		# Getting all column names except 'Flower Name'
		effect_columns = [col for col in df.columns if col != 'Flower Name']
		for col in ing_df.columns:
			ing_df[col] = ing_df[col].apply(lambda x: str(x).lower().replace(" ", "_"))

		unique_effects = set()
		for col in effect_columns:
			unique_effects.update(df[col].dropna().unique())
		pprint.pprint(unique_effects)
		return list(unique_effects)

	def get_effects_from_ingredient(self, ingredient_name):
		pass

	#need these sort of "helper functions" to sort out the particulars to get the numbers right	
	def gen_fac(self,effect_type):
		pass

	def calculate_ins_str(self,thing):
		if thing == "novice":
			return 0.1
		elif thing == "apprentice":
			return 0.25
		elif thing == "journeyman":
			return 0.5
		elif thing == "expert":
			return 0.75
		elif thing == "master":
			return 1
		else:
			raise Exception(f"Incorrect Insturment Level Given you asked for {thing} must be one of the class instance arguments")

	def calculate_strength(self):
		if alchemy_level == "novice":
			return 0.1
		elif alchemy_level == "apprentice":
			return 0.25
		elif alchemy_level == "journeyman":
			return 0.5
		elif alchemy_level == "expert":
			return 0.75
		elif alchemy_level == "master":
			return 1
		else:
			raise Exception(f"Incorrect Alchemy Level Given you asked for {thing} must be one of the class instance arguments")


	def calculate_potion_duration_magnitude(self, ing_list:list, Base_Mag=1,Base_Dur=1):
		Base_Mag = ((self.effective_alchemy_level() + self.calculate_strength*25)/(Effect_Base_Cost/10 * 4)) ** (1/2.28)
		Base_Dur = 4 * Base_Mag

		# need to set Alem_Fac, Ret_Mag_Fac, Ret_Dur_Fac, Calc_Fac for one of three cases:

		# for i in ing_list:
		# 	if 

		Magnitude = Base_Mag * (1 + Calc_Fac*Calcinator_Strength + Ret_Mag_Fac*Retort_Strength- Alem_Fac*Alembic_Strength)
		Duration = Base_Dur * (1 + Calc_Fac*Calcinator_Strength + Ret_Dur_Fac*Retort_Strength- Alem_Fac*Alembic_Strength)

	def potion_generator(self):
		magicka_cost = self.effective_alchemy_lvl + self.calculate_strength()*25
		magnitude = Base_Mag * (1 + Calc_Fac)

		#any potion with even a single positive effect will make a potion
		#any potion with exclusively negative effects will produce a poison.




#x = AlchemyFactory().get_effects_from_ingredients(['Sweetcake','Apple'])
x = AlchemyFactory()
get_unique_effects()