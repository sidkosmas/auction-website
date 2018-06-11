from . import views
from django.urls import path

app_name = 'website'

urlpatterns = [
	path('', views.index, name='index'),
	path('register/', views.register, name='register'),
	path('login/',views.login, name='login'),
    path('profile/',views.profile, name='profile'),
    path('bid/',views.bid, name='bid'),

]
