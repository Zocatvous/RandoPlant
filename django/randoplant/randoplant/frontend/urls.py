from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
	path('home/', include('home.urls'))
	path('admin/', admin.site.urls),
    path('randoplant-home/', views.randoplant_home, name='randoplant-home'),
]

