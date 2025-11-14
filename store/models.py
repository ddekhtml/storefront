from django.db import models
from django.core.validators import MinValueValidator
from uuid import uuid4
from django.conf import settings
from django.contrib import admin
# Create your models here.
class Promotion(models.Model):
    description = models.TextField()
    doscount= models.FloatField()

class Collection(models.Model):
    title = models.CharField(max_length=255, unique=True)
    
    def __str__ (self):
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2, 
        validators=[MinValueValidator(0.01, message= "The unit price should be greater than 0.01")])
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT )
    promotion = models.ManyToManyField(Promotion, blank=True)
    def __str__(self):
        return self.title
    
class Customer(models.Model):
    MEMBERSHIP_CHOICES = [
        ('B', "Bronze"),
        ('S', 'Silver'), 
        ('G', 'Gold')
    ]
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default='B')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['user__first_name', 'user__last_name']
        permissions=[
            ('view_history', 'Can view history'),
        ]
        

    @admin.display(ordering="user__first_name")
    def first_name(self):
        return self.user.first_name
    
    def last_name(self):
        return self.user.last_name
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Address (models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    zip = models.CharField(max_length=255)


class Cart(models.Model):
    id = models.CharField(
        primary_key=True,
        default=uuid4, 
        editable=False, 
        max_length=36)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItems (models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', max_length=36)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )

    class Meta:
        unique_together =[["cart", "product"]]

class Order(models.Model):
    PAYMENT_STATUS_CHOICES = [
        (
            'P', 'Pending'
        ), 
        (
            'C', 'Complete'
        ), 
        (
            'F', 'Failed'
        )
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status= models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default='P')
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    class Meta:
        permissions=[ 
            ('cancel_order', "Can cancel order")
        ]

class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    def __str__ (self):
        return f"{self.order.placed_at}"

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)