from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, AuctionListing, ItemType, Comments,Bids


def index(request):
    allcatagories = ItemType.objects.all()
    activelisting= AuctionListing.objects.filter(active=True)
    return render(request, "auctions/index.html", {
        "listing": activelisting,
        "categories": allcatagories,
    })

def winnerallert(request):
    currentuser= request.user
    itemallclosed = AuctionListing.objects.filter(active=False)
    return render(request, "auctions/winnerallert.html", {
        "listing": itemallclosed,
    })


def closeauction(request, id):
    #closing auction
    item = AuctionListing.objects.get(pk=id)
    item.active= False
    item.save()
    #winner
    #winner = item.price.userbidding

    #see it added to watchlist or not(boolian)
    listingInWatchlist= request.user in item.watchlist.all()
    #fillter all commnets that belongs to thid item
    allcoments= Comments.objects.filter(item=item)
    isOwner= request.user.username ==item.owner.username

    return render(request, "auctions/listing.html", {
        "item": item,
        "isWatchlisted": listingInWatchlist,
        "comments" : allcoments,
        "isOwner" : isOwner,
        "update" : True,
        "message": "You successfully closed the auction for this item in finnal price "
    })


def addnewbid(request, id):
    newbid= request.POST["bid"]
    item = AuctionListing.objects.get(pk=id)

    #see it added to watchlist or not(boolian)
    listingInWatchlist= request.user in item.watchlist.all()
    #fillter all commnets that belongs to thid item
    allcoments= Comments.objects.filter(item=item)

    if int(newbid) > item.price.bid:
        # creat new Bids object 
        updatebid= Bids(
            userbidding= request.user,
            bid= newbid
        )
        updatebid.save()
        item.price = updatebid
        item.save()
        return render(request, "auctions/listing.html",{
            "item":item,
            "message": "successful bid",
            "update" : True,
            "isWatchlisted": listingInWatchlist,
            "comments" : allcoments,
        })
    else:
        return render(request, "auctions/listing.html",{
            "item":item,
            "message": "Your bid is lower than the current price",
            "update" : False,
            "isWatchlisted": listingInWatchlist,
            "comments" : allcoments,
        })



def addnewcomment(request, id):
    currentuser= request.user
    item= AuctionListing.objects.get(pk=id)
    message= request.POST["commnent"]

    newComment = Comments(
    writer= currentuser,
    item = item,
    message= message
    )
    newComment.save()
    return HttpResponseRedirect(reverse( "listing", args=(id, )))





def displaycategory(request):
     if request.method =="POST":
        #get the type from the form
        categoryFromForm= request.POST["categories"]
        #take the database instance of the same type
        category = ItemType.objects.get(typeName=categoryFromForm)
            
        allcatagories = ItemType.objects.all()
        activelisting= AuctionListing.objects.filter(active=True, type= category)
        return render(request, "auctions/index.html", {
            "listing": activelisting,
            "categories": allcatagories,

        })
     

def listing(request, id):
    item = AuctionListing.objects.get(pk=id)
    #see it added to watchlist or not(boolian)
    listingInWatchlist= request.user in item.watchlist.all()
    #fillter all commnets that belongs to thid item
    allcoments= Comments.objects.filter(item=item)
    # for closing bids we need to know the owner
    isOwner= request.user.username ==item.owner.username

    return render(request, "auctions/listing.html", {
        "item": item,
        "isWatchlisted": listingInWatchlist,
        "comments" : allcoments,
        "isOwner" : isOwner,
    })

def addwatchlist(request, id):
    listeddata= AuctionListing.objects.get(pk=id)
    currentuser= request.user
    listeddata.watchlist.add(currentuser)
    return HttpResponseRedirect(reverse( "listing", args=(id, )))

def removewatchlist(request, id):
    listeddata= AuctionListing.objects.get(pk=id)
    currentuser= request.user
    listeddata.watchlist.remove(currentuser)
    return HttpResponseRedirect(reverse( "listing", args=(id, )))


def displaywatchlist(request):
    currentuser = request.user
    listeditem= currentuser.watchlist.all()
    return render(request, "auctions/displaywatchlist.html",{
        "listing":listeditem
    })

    



def createItemType(request):
    if request.method == "GET":
        allcatagories = ItemType.objects.all()
        return render(request, "auctions/createitem.html", {
            "categories": allcatagories,

        })
    else:
        #get data from the form
        title = request.POST["title"]
        description = request.POST["description"]
        imageUrl = request.POST["imageUrl"]
        price = request.POST["price"]
        categories = request.POST["categories"]
        # get the user
        currentuser= request.user
        #category table object
        category = ItemType.objects.get(typeName= categories)
        #create a Bids object
        bid = Bids(
            bid=int(price),
            userbidding=currentuser
            )
        bid.save()


        #create a new auctionlisting object
        newlisting = AuctionListing(
            title  = title,
            about = description,
            imageurl = imageUrl,
            price = bid,
            active= True,
            owner = currentuser,
            type = category
        )

        #save 
        newlisting.save()
        return HttpResponseRedirect(reverse("index"))



    


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
