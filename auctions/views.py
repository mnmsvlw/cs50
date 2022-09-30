from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import User, Categorie, Item, Bid, Watchlist, Comment


def index(request):
    if Item.objects.filter(status='Opened').exists():
        items = Item.objects.filter(status='Opened').order_by('-id')
        full = []
        numbers = []
        for item in items:
            if Bid.objects.filter(item = item).exists():
                bids = {}
                bids["item"] = item.id
                bids["bid"] = Bid.objects.filter(item = item).order_by('-bid')[0].bid
                full.append(bids)
                numbers.append(item.id)
        return render(request, "auctions/index.html", {
            "items": items,
            "bids": full,
            "numbers" : numbers

        })
    else:
        return render(request, "auctions/index.html")


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

@login_required
def create(request):

    if request.method == 'POST':

        item = Item()
        item.name = request.POST['title']
        item.text = request.POST['description']
        item.url = request.POST['url']
        item.category_id = Categorie.objects.get(name=request.POST['category']).id
        item.start_bid = request.POST['startingbid']
        item.owner = User.objects.get(id=request.user.id)
        item.save()

        # listing = Listing()
        # listing.username = User.objects.get(id=request.user.id)
        # listing.item = Item.objects.get(id=item.id)
        # # listing.username = User.objects.get(id=request.user.id)
        # # listing.item = Item.objects.get(name=request.POST['title'])
        # listing.save()
        items = Item.objects.all()
        return render(request, "auctions/index.html", {
            "items": items,
            "message": "Your item was successfully listed!"
        })
        
    else:
        category = Categorie.objects.all()
        return render(request, 'auctions/create.html', {
            'categories': category
        })

def card(request, item_id):

    if request.method == 'POST':
        
        if 'bid' in request.POST:
            bid = Bid()
            bid.bid = request.POST['bid']
            bid.username = User.objects.get(id=request.user.id)
            bid.item = Item.objects.get(id=request.POST['id'])
            bid.save()

        if 'watch' in request.POST:
            watchlist = Watchlist()
            watchlist.username = User.objects.get(id=request.user.id)
            watchlist.item = Item.objects.get(id=request.POST['watch'])
            watchlist.save()

        if 'unwatch' in request.POST:
            unwatch = Watchlist.objects.get(username=request.user.id, item=request.POST['unwatch'])
            unwatch.delete()
        
        if 'close' in request.POST:
            close = Item.objects.get(id=request.POST['close'])
            close.status = 'Closed'
            close.save()
        
        if 'comment' in request.POST:
            comment = Comment()
            comment.comment = request.POST['comment']
            comment.username = User.objects.get(id=request.user.id)
            comment.item = Item.objects.get(id=request.POST['itemidcom'])
            comment.save()

        if 'remcom' in request.POST:
            comment = Comment.objects.get(id=request.POST['remcom'])
            comment.delete()

    cards = Item.objects.get(id=item_id)

    if Bid.objects.filter(item = item_id).exists():
        bids = Bid.objects.filter(item = item_id).order_by('-bid')[0]
        count = Bid.objects.filter(item = item_id).count
    else:
        bids = None
        count = None

    if Watchlist.objects.filter(item=item_id, username=request.user.id):
        watchlist = True
    else:
        watchlist = False
    
    if Comment.objects.filter(item=item_id):
        comments = Comment.objects.filter(item=item_id)
    else:
        comments = None


    return render(request, 'auctions/itempage.html', {
            "items": cards,
            "bids" : bids,
            "watchlist": watchlist,
            "comments" : comments,
            "count": count
        })

@login_required
def watchlist(request):

    watchlist = Watchlist.objects.filter(username=request.user.id)
    items = Item.objects.filter(status='Opened')
    full = []
    numbers = []
    for item in items:
        if Bid.objects.filter(item = item).exists():
            bids = {}
            bids["item"] = item.id
            bids["bid"] = Bid.objects.filter(item = item).order_by('-bid')[0].bid
            full.append(bids)
            numbers.append(item.id)
    return render(request, 'auctions/watchlist.html', {
        "watchlist": watchlist,
        "bids": full,
        "numbers": numbers
    })


def categories(request):

    categories = Categorie.objects.all()
    return render(request, 'auctions/categories.html', {
        "categories": categories
    })

def cat(request, category):

    category = Categorie.objects.get(name=category)
    items = Item.objects.filter(category=category.id)

    return render(request, 'auctions/category.html', {
        "items": items,
        "category": category
    })