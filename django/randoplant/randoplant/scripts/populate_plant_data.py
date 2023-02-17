import re
from django.apps import apps
from django.conf import settings
from django.core.management import call_command
from .models import Plant
from .plant import PlantUtilities


def extract_substring(string):
    match = re.search(r'/bias/(.*?)_bias', string)
    if match:
        return match.group(1)
    else:
        return None


def create_plant(series):
    Plant.objects.create(
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
    )


# Truncate the Plant table
Plant.objects.all().delete()

# Create the plants
plant_utilities = PlantUtilities('Centriss')
frames = plant_utilities._plant_bias_obj

for continent, frame in frames.items():
    print(f'Working on {continent}')
    for col, series in frame['_dataframe'].iteritems():
        if (series[0] == 'Common value'):
            continue
        else:
            print(f'Inserting {series[1]}')
            create_plant(series, apps.get_model('randoplant', 'Continent').objects.get(name=continent).id)
    print('Finished continent:', continent)

# Call `refresh_from_db()` on each instance to ensure the correct `continent_origin` value is retrieved
for plant in Plant.objects.all():
    plant.refresh_from_db()
