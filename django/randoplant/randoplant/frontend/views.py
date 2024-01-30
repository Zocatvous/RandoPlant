# frontend/views.py
from django.views.generic import TemplateView
from django.shortcuts import render
from django.randoplant.models import Plant



def home(request):
	"""View function for home page of site."""
	#list queries to be returned by the view??
	num_plants = Plant.objects.all().count()

	render()




def randoplant_home(request):
	num_plants = Plant.objects.all().count()
	plant_1 = Plant.objects.all().first()
	context = {
		'plant_1': plant_1,
		'num_plants': num_plants,

	}

    return render(request, 'templates/randoplant_home.html')

####################### MANAGEMENT #################################

class PlantPageView(TemplateView):
    template_name = 'randoplant_home.html'