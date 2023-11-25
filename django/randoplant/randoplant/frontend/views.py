# frontend/views.py
from django.views.generic import TemplateView
from django.shortcuts import render

def randoplant_home(request):
    return render(request, 'templates/randoplant_home.html')

####################### MANAGEMENT #################################

class PlantPageView(TemplateView):
    template_name = 'randoplant_home.html'