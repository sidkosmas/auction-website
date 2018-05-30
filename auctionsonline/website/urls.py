from . import views
from django.urls import path

app_name = 'website'

urlpatterns = [
	path('', views.index, name='index')
]
