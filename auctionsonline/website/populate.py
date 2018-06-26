# on django shell 
#    $ exec(open('website/populate.py').read())

# This script populates the database with products, users, and auctions.
# The first auction starts one minute after executing this script.

from django.core.files import File
from website.models import *
from django.utils import timezone
from datetime import timedelta
import sqlite3
import shutil

Product.objects.all().delete()
User.objects.all().delete()
Auction.objects.all().delete()

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()
c.execute("UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='website_product'")
c.execute("UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='website_user'")
c.execute("UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='website_auction'")
conn.commit()
conn.close()
shutil.rmtree('media/images/')

a = Product()
a.title = "PS4 Pro 1TB"
a.description = "Sony's PlayStation 4 Pro 1TB"
a.quantity = 8
a.category = "CON"
a.image.save('console-01.png', File(open('website/static/images/products/console-01.png', 'rb')))

a = Product()
a.title = "PS4 Slim 500GB (Gold)"
a.description = "Sony's PlayStation 4 Slim 500GB Gold Edition"
a.quantity = 1
a.category = "CON"
a.image.save('console-02.png', File(open('website/static/images/products/console-02.png', 'rb')))

a = Product()
a.title = "Xbox One X 1TB"
a.description = "Microsoft's Xbox One X 1TB"
a.quantity = 4
a.category = "CON"
a.image.save('console-03.png', File(open('website/static/images/products/console-03.png', 'rb')))

a = Product()
a.title = "Nintendo Switch 32GB"
a.description = "Nintendo's Switch 32GB"
a.quantity = 10
a.category = "CON"
a.image.save('console-04.png', File(open('website/static/images/products/console-04.png', 'rb')))

a = Product()
a.title = "Xiaomi SmartWatch X"
a.description = "Xiaomi's latest SmartWatch"
a.quantity = 3
a.category = "GAD"
a.image.save('gadget-01.png', File(open('website/static/images/products/gadget-01.png', 'rb')))

a = Product()
a.title = "Doodo 35LMS"
a.description = "Another SmartWatch"
a.quantity = 1
a.category = "GAD"
a.image.save('gadget-02.png', File(open('website/static/images/products/gadget-02.png', 'rb')))

a = Product()
a.title = "OEG 3D Projector"
a.description = "3D Projector for model presentations"
a.quantity = 1
a.category = "GAD"
a.image.save('gadget-03.png', File(open('website/static/images/products/gadget-03.png', 'rb')))

a = Product()
a.title = "Wireless Controller"
a.description = "A bluetooth wireless controller for your computer"
a.quantity = 2
a.category = "GAD"
a.image.save('gadget-04.png', File(open('website/static/images/products/gadget-04.png', 'rb')))

a = Product()
a.title = "Bloodborne (PS4)"
a.description = "Bandai Games Bloodborne for PS4"
a.quantity = 5
a.category = "GAM"
a.image.save('game-01.png', File(open('website/static/images/products/game-01.png', 'rb')))

a = Product()
a.title = "Uncharted 4 (PS4)"
a.description = "Naughty Dog's Uncharted 4 for PS4"
a.quantity = 2
a.category = "GAM"
a.image.save('game-02.png', File(open('website/static/images/products/game-02.png', 'rb')))

a = Product()
a.title = "Marvel V.S. Capcom Infinite (PS4)"
a.description = "Capcom's latest fighting game for PS4"
a.quantity = 1
a.category = "GAM"
a.image.save('game-03.png', File(open('website/static/images/products/game-03.png', 'rb')))

a = Product()
a.title = "Sea of Thieves (XONE)"
a.description = "Sea Game for Xbox One"
a.quantity = 1
a.category = "GAM"
a.image.save('game-04.png', File(open('website/static/images/products/game-04.png', 'rb')))

a = Product()
a.title = "Call of Duty WWII (XONE)"
a.description = "Another Call of Duty game for Xbox One"
a.quantity = 1
a.category = "GAM"
a.image.save('game-05.png', File(open('website/static/images/products/game-05.png', 'rb')))

a = Product()
a.title = "HP Laptop XMS4"
a.description = "HP Laptop"
a.quantity = 2
a.category = "LAP"
a.image.save('laptop-01.png', File(open('website/static/images/products/laptop-01.png', 'rb')))

a = Product()
a.title = "Dell Laptop LL32"
a.description = "Dell Laptop"
a.quantity = 2
a.category = "LAP"
a.image.save('laptop-02.png', File(open('website/static/images/products/laptop-02.png', 'rb')))

a = Product()
a.title = "MSI Laptop x322"
a.description = "MSI Laptop"
a.quantity = 5
a.category = "LAP"
a.image.save('laptop-03.png', File(open('website/static/images/products/laptop-03.png', 'rb')))

a = Product()
a.title = "Macbook Air 444"
a.description = "MAC Laptop"
a.quantity = 2
a.category = "LAP"
a.image.save('laptop-04.png', File(open('website/static/images/products/laptop-04.png', 'rb')))

a = Product()
a.title = "Sony 40'' Ultimate 3"
a.description = "Sony Television"
a.quantity = 1
a.category = "TEL"
a.image.save('tv-01.png', File(open('website/static/images/products/tv-01.png', 'rb')))

a = Product()
a.title = "Samsung Curved 50'' LPS4"
a.description = "Samsung Television"
a.quantity = 4
a.category = "TEL"
a.image.save('tv-02.png', File(open('website/static/images/products/tv-02.png', 'rb')))

a = Product()
a.title = "LG 42'' LG35WF3"
a.description = "LG Television"
a.quantity = 1
a.category = "TEL"
a.image.save('tv-03.png', File(open('website/static/images/products/tv-03.png', 'rb')))

a = Product()
a.title = "LG 50'' LG40WF3"
a.description = "LG Television"
a.quantity = 1
a.category = "TEL"
a.image.save('tv-04.png', File(open('website/static/images/products/tv-04.png', 'rb')))

a = Product()
a.title = "Sony 60'' SN0WF3"
a.description = "SONY Television"
a.quantity = 0
a.category = "TEL"
a.image.save('tv-05.png', File(open('website/static/images/products/tv-05.png', 'rb')))

b = User()
b.username = "dummy1"
b.email = "dummy1@mail.com"
b.password = "dummypassword"
b.balance = 20.0
b.firstname = "Dummy"
b.lastname = "One"
b.cellphone = "6988757575"
b.address = "Dumadd 199"
b.town = "Dummtown"
b.post_code = "35100"
b.country = "Dummcon"
b.save()

b = User()
b.username = "dummy2"
b.email = "dummy2@mail.com"
b.password = "dummypassword"
b.balance = 20.0
b.firstname = "Dummy"
b.lastname = "Two"
b.cellphone = "6933357575"
b.address = "Dumadd 299"
b.town = "Dummtown"
b.post_code = "35100"
b.country = "Dummcon"
b.save()

b = User()
b.username = "dummy3"
b.email = "dummy3@mail.com"
b.password = "dummypassword"
b.balance = 20.0
b.firstname = "Dummy"
b.lastname = "Three"
b.cellphone = "6911757575"
b.address = "Dumadd 199"
b.town = "Dummtown"
b.post_code = "35100"
b.country = "Dummcon"
b.save()

b = User()
b.username = "dummy4"
b.email = "dummy4@mail.com"
b.password = "dummypassword"
b.balance = 20.0
b.firstname = "Dummy"
b.lastname = "Four"
b.cellphone = "6984457575"
b.address = "Dumadd 499"
b.town = "Dummtown"
b.post_code = "35100"
b.country = "Dummcon"
b.save()

c = Auction()
d = Product.objects.filter(id=1)
c.product_id = d[0]
c.number_of_bids = 0
c.time_starting  = timezone.now() + timedelta(minutes=1)
c.time_ending = timezone.now() + timedelta(minutes=6)
c.save()

c = Auction()
d = Product.objects.filter(id=9)
c.product_id = d[0]
c.number_of_bids = 0
c.time_starting = timezone.now() + timedelta(minutes=2)
c.time_ending = timezone.now() + timedelta(minutes=7)
c.save()

c = Auction()
d = Product.objects.filter(id=10)
c.product_id = d[0]
c.number_of_bids = 0
c.time_starting = timezone.now() + timedelta(hours=1)
c.time_ending  = timezone.now() + timedelta(hours=1) + timedelta(minutes=5)
c.save()

c = Auction()
d = Product.objects.filter(id=5)
c.product_id = d[0]
c.number_of_bids = 0
c.time_starting = timezone.now() + timedelta(days=1)
c.time_ending = timezone.now() + timedelta(days=1) + timedelta(minutes=5)
c.save()

c = Auction()
d = Product.objects.filter(id=12)
c.product_id = d[0]
c.number_of_bids = 0
c.time_starting = timezone.now() + timedelta(days=1) + timedelta(hours=2)
c.time_ending = timezone.now() + timedelta(days=1) + timedelta(hours=2) + timedelta(minutes=5)
c.save()

c = Auction()
d = Product.objects.filter(id=14)
c.product_id = d[0]
c.number_of_bids = 0
c.time_starting = timezone.now() + timedelta(days=1) + timedelta(hours=4)
c.time_ending = timezone.now() + timedelta(days=1) + timedelta(hours=4) + timedelta(minutes=5)
c.save()

c = Auction()
d = Product.objects.filter(id=18)
c.product_id = d[0]
c.number_of_bids = 0
c.time_starting = timezone.now() + timedelta(days=1) + timedelta(hours=6)
c.time_ending = timezone.now() + timedelta(days=1) + timedelta(hours=6) + timedelta(minutes=5)
c.save()

c = Auction()
d = Product.objects.filter(id=19)
c.product_id = d[0]
c.number_of_bids = 0
c.time_starting = timezone.now() + timedelta(days=2)
c.time_ending = timezone.now() + timedelta(days=2) + timedelta(minutes=5)
c.save()

c = Auction()
d = Product.objects.filter(id=4)
c.product_id = d[0]
c.number_of_bids = 0
c.time_starting = timezone.now() + timedelta(days=2) + timedelta(hours=2)
c.time_ending = timezone.now() + timedelta(days=2) + timedelta(hours=2) + timedelta(minutes=5)
c.save()
