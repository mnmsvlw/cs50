from django.contrib import admin

from .models import User, Item, Categorie, Bid, Comment, Watchlist

# Register your models here.
admin.site.register(User)
admin.site.register(Item)
# admin.site.register(Listing)
admin.site.register(Categorie)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Watchlist)

