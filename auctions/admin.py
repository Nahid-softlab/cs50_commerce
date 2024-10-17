from django.contrib import admin
from .models import User, ItemType, AuctionListing,Comments,Bids
# Register your models here.

admin.site.register(User)
admin.site.register(ItemType)
admin.site.register(AuctionListing)
admin.site.register(Comments)
admin.site.register(Bids)