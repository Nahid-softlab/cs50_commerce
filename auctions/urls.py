from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path( "create", views.createItemType, name="create"),
    path("displaycategory", views.displaycategory, name="displaycategory"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("removewatchlist/<int:id>", views.removewatchlist, name="removewatchlist"),
    path("addwatchlist/<int:id>", views.addwatchlist, name="addwatchlist"),
    path("displaywatchlist", views.displaywatchlist, name="displaywatchlist"),
    path("addnewcomment/<int:id>", views.addnewcomment, name="addnewcomment"),
    path("addnewbid/<int:id>", views.addnewbid, name="addnewbid"),
    path("closeauction/<int:id>", views.closeauction, name="closeauction"),
    path("winnerallert", views.winnerallert, name="winnerallert")
]
