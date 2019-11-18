from django.contrib import admin
from .models import UserDetails, Product, Auction, Chat, Watchlist, Bid

#Username : admin
#Password : administrator

# Register your models here.
admin.site.register(UserDetails)
admin.site.register(Product)
admin.site.register(Auction)
admin.site.register(Chat)
admin.site.register(Watchlist)
admin.site.register(Bid)