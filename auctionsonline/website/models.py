from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
	email = models.EmailField()
	balance = models.DecimalField(max_digits=10, decimal_places=2)
	firstname = models.CharField(max_length=255)
	lastname = models.CharField(max_length=255)
	cellphone = models.CharField(max_length=12)
	address = models.CharField(max_length=255)
	town = models.CharField(max_length=255)
	post_code = models.CharField(max_length=20)
	country = models.CharField(max_length=255)

class Product(models.Model):
	title = models.CharField(max_length=255)
	image = models.ImageField()
	description = models.CharField(max_length = 500)
	quantity = models.IntegerField()

class Wishlist(models.Model):
	user_id = ForeignKey(Users, on_delete=models.CASCADE)
	product_id = ForeignKey(Product, on_delete=models.CASCADE)

