from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class ItemType(models.Model):
    typeName = models.CharField(max_length=30)

    def __str__(self) :
        return self.typeName

class Bids(models.Model):
    bid = models.IntegerField(default=0)
    userbidding= models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True, related_name="userbidding")
    


class AuctionListing(models.Model):
    title  = models.CharField(max_length=30)
    about = models.CharField(max_length=200)
    imageurl = models.CharField(max_length=1000, default="No Image")
    price = models.ForeignKey(Bids, on_delete=models.CASCADE, blank=True,null=True, related_name="bidprice" )
    active= models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,null=True, related_name="user")
    type = models.ForeignKey(ItemType, on_delete=models.CASCADE , blank=True, null=True, related_name="itemtype")
    watchlist=models.ManyToManyField(User, blank=True, null=True, related_name="watchlist")


    



class Comments(models.Model):
    writer= models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,related_name="author")
    item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, blank=True, null=True,related_name="itemofcmt" )
    message= models.CharField(max_length=300, default="You didn't wrote anything")

    def __str__(self):
        return f"{self.writer} comment on {self.item}"