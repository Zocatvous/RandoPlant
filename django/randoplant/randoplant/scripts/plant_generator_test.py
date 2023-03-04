def check_value_rounding():
	plants_list = []
	for i in range(1000):
		plants_list.append(PlantObject(plant=Plant.select_plant_by_region(region='tentacular')))
		print(f'Gen.d {i} plants\r',end='\r')
		print('\n')
	sorted_plants = sorted(plants_list, key=lambda x: x.potence, reverse=True)
	print(sorted_plants[:10])


def main():
	check_value_rounding()

if __name__ == "__main__":
	main()