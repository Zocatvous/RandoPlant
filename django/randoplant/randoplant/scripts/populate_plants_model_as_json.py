import sys
import os
module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(module_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "randoplant.settings")
import django
django.setup()
from django.core import serializers
from randoplant.models import Plant, Size, Region
import datetime

def dump_to_json(model,filename):
	now = datetime.datetime.now()
	data = model.objects.all()
	json_data = serializers.serialize('json',data)
	with open(f'../json/dumps/{now.strftime("%Y-%m-%d_%H-%M-%S")}_{filename}.json', 'w+') as file:
		file.write(json_data)

dump_to_json(Plant,'test_plants_dump')