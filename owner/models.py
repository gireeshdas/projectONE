from distutils.command.upload import upload
from itertools import product
from optparse import Option
from pyexpat import model
from ssl import Options
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.

class Categories(models.Model):
    category_name = models.CharField(max_length=200, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.category_name


class Products(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE,null=True)
    image = models.ImageField(upload_to="images", null=True)
    price = models.PositiveIntegerField()
    description = models.CharField(max_length=250, null=True)

    def __str__(self):
        return self.product_name


class Carts(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now=True, null=True)
    Options = (
        ("in-cart", "in-cart"),
        ("order-placed", "order-placed"),
        ("cancelled", "cancelled")
    )
    status = models.CharField(max_length=120, choices=Options, default="in-cart")
    qty = models.PositiveIntegerField(default=1)


class Order(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now=True, null=True)
    Options = (
        ("order-placed", "order-placed"),
        ("dispatched", "dispatched"),
        ("in-transit", "in-transit"),
        ("delivered", "delivered"),
        ("cancelled", "cancelled")
    )
    status = models.CharField(max_length=120, choices=Options, default="order-placed")
    delivery_address=models.CharField(max_length=250,null=True)
    expected_delivery_date=models.DateTimeField(null=True)


class Reviews(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comments = models.CharField(max_length=200)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])





