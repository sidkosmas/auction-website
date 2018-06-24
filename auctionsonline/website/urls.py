from . import views
from django.urls import path

app_name = 'website'

urlpatterns = [
	path('', views.index, name='index'),
	path('login/', views.login_page, name='login_view'),
	path('home/logout/', views.logout_page, name='logout_view'),
	path('home/', views.home_page, name='home_view'),
	path('register/', views.register, name='register'),
	path('register/register_v2/', views.register_page, name='register_page'),
    path('profile/',views.profile, name='profile'),
    path('<str:category>/', views.filter_auctions, name='filter_auctions') # to fix

]
