from . import views
from django.urls import path

app_name = 'website'

urlpatterns = [
	path('', views.index, name='index'),
	path('', views.register, name='register'),
	path('',views.login, name='login'),
    path('',views.profile, name='profile'),
    path('',views.bid, name='bid'),

]
