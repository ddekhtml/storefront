from django.db import models
from django.core.validators import MinValueValidator
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
    first_name = models.CharField(max_length=255)
    last_name= models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default='B')

    class Meta:
        db_table = "store_customers"
        indexes = [
            models.Index (fields=['first_name', 'last_name'])
        ]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Address (models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    zip = models.CharField(max_length=255)

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class CartItems (models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

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
    payment_status= models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
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