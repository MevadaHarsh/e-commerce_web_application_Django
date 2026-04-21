from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    category_name=models.CharField(max_length=20)
    images=models.ImageField(upload_to='static/image/')

    def __str__(self):
        return f"{self.category_name}"
    
class Product(models.Model):
    category=models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    product_name=models.CharField(max_length=50, null=True, blank=True)
    image=models.ImageField(upload_to='static/image/')
    price=models.IntegerField(null=True, blank=True)
    count=models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.product_name}"
    
class ContactUs(models.Model):
    name=models.CharField(max_length=100, null=True, blank=True)
    email=models.CharField(max_length=100, null=True, blank=True)
    subject=models.CharField(max_length=500, null=True, blank=True)
    message=models.TextField()

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
class CartItem(models.Model):
    Cart=models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', null=True, blank=True)
    Product=models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity=models.IntegerField(default=0, null=True, blank=True)

    def total_price(self):
        return self.Product.price * self.quantity
    
    def __str__(self):
        return f"{self.Product.product_name}"