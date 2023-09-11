from rest_framework import serializers
from .models import Plant


class PlantSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Plant
		#fields = (some imported variable that contains all the plant fields - i used something like this to drop all the non-float fields on the Plant model)