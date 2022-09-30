from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Categorie(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'


class Item(models.Model):
    name = models.CharField(max_length=20)
    text = models.CharField(max_length=256)
    category = models.ForeignKey(Categorie, on_delete=models.PROTECT, related_name='cat')
    url = models.CharField(max_length=256, blank=True)
    start_bid = models.DecimalField(max_digits=10,decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    status = models.CharField(max_length=10, default='Opened')

    def __str__(self):
        return f"{self.name}"


class Bid(models.Model):
    bid = models.DecimalField(max_digits=10,decimal_places=2)
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='placer')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='positionbid')

    def __str__(self):
        return f'{self.bid}'


class Comment(models.Model):
    comment = models.CharField(max_length=1024)
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commenter')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='positioncom')
    time = models.TimeField(auto_now=True)

    def __str__(self):
        return f'{self.username} is commenting {self.comment} on {self.item}'

class Watchlist(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watcher')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='positionwatch')

    def __str__(self):
        return f'{self.username} is watching {self.item}'

