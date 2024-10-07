from django.db import models
from account.models import CustomUser as User
from product.models import Product
# Create your models here.

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =  models.DateTimeField(auto_now=True)
    _total_price = None 
     
    def __str__(self):
        return str(self.user)
    
  

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_item')
    quantity = models.IntegerField()
    price  = models.DecimalField(max_digits=5, decimal_places=2)

    
    def __str__(self):
        return f"{self.cart}"
   