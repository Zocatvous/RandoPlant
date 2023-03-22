import pandas as pd
# pd.set_option('display.max_columns', None)
def construct_all_ingredients_df():
	ob = pd.read_excel('./all_ob_ingredients.xlsx')
	column_labels = ['Name','Effect_1','Effect_2','Effect_3','Effect_4','Price','Wieght','Harvest_probability']
	ingredients_df = pd.DataFrame(columns=column_labels)
	new_vals = []
	for i, row in ob.iterrows():
		if i % 3 == 0:
			name=row[1]
			#print(f'Effect1:{ob.loc[i+2][2]} Effect2:{ob.loc[i+2][3]} Effect3:{ob.loc[i+2][4]} Effect4:{ob.loc[i+2][5]} Price:{ob.loc[i+2][6]} Wieght:{ob.loc[i+2][7]} HarvestProb:{ob.loc[i+2][8]}')
			ef1 = ob.loc[i+2][2]
			ef2 = ob.loc[i+2][3]
			ef3 = ob.loc[i+2][4]
			ef4 = ob.loc[i+2][5]
			pr = ob.loc[i+2][6]
			wie = ob.loc[i+2][7]
			har = ob.loc[i+2][8]
			ingredients_df = ingredients_df.append([{'Name':name, 'Effect_1':ef1, 'Effect_2':ef2, 'Effect_3':ef3, 'Effect_4':ef4, 'Price':pr, 'Wieght':wie, 'Harvest_probability':har}])
	return ingredients_df.reset_index(drop=True)

all_ingredients = construct_all_ingredients_df()
print(all_ingredients)

class AlchemyFactory:
	def __init__(self,  alembic_level=1, calcinator_level=1,pestlemortar_level=1, retort_level=1, ingredients:list):
		self.al = 1
		self.duration_only_effects_list = []
		self.magnitude_only_effects_list = []
		self.

	def alembic(self):


	def calculate_potion_duration_magnitude(self, Base_Mag=1,Base_Dur=1)
		Base_Mag = ((Effective_Alchemy + MortarPestle_Strength*25)/(Effect_Base_Cost/10 * 4)) **  (1/2.28)
		Base_Dur = 4 * Base_Mag
		Magnitude = Base_Mag * (1 + Calc_Fac*Calcinator_Strength + Ret_Mag_Fac*Retort_Strength- Alem_Fac*Alembic_Strength)
		Duration = Base_Dur * (1 + Calc_Fac*Calcinator_Strength + Ret_Dur_Fac*Retort_Strength- Alem_Fac*Alembic_Strength)