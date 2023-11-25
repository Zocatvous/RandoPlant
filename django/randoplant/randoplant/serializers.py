from rest_framework import serializers
from rest_framework.decorators import api_view
from .models import Plant, PlantObject


class PlantObjectSerlializer(serializers.Serializer):
	name = serializers.CharField()
	size = serializers.CharField()
	extremeness = serializers.IntegerField()
	potence = serializers.IntegerField()
	value = serializers.IntegerField()
	affinities = serializers.DictField()

	def to_representation(self, instance):
		data = super().to_representation(instance)
		data['affinities'] = instance.affinities
		return data

@api_view(['GET'])
def plant_object_detail(request, pk):
    try:
        plant_object = PlantObject.objects.get(pk=pk)
    except PlantObject.DoesNotExist:
        return Response(status=404, data={'message': 'Something went wrong'})

    serializer = PlantObjectSerializer(plant_object)
    return Response(serializer.data)


class PlantObjectSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Plant
		#fields = (some imported variable that contains all the plant fields - i used something like this to drop all the non-float fields on the Plant model)