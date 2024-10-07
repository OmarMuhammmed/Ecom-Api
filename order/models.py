from django.db import models
from account.models import CustomUser as User
from product.models import Product 


class OrderStatus(models.TextChoices):
    PROSSING = 'Prossing'
    SHIPPED = 'SHIPPED'
    DELEVERD = 'Deleverd'

   
class PaymentStatus(models.TextChoices):
    PAID = 'Paid'
    UNPAID = 'Unpaid'

class PaymentMethod(models.TextChoices):
    COD = 'COD'
    ONLINE = 'STRIPE'

# The final Order
class Order(models.Model):
    city = models.CharField(max_length=100, blank=False, default="")
    zip_code = models.CharField( max_length=50)
    street = models.CharField (max_length=500, blank=False, default="")
    state = models.CharField(max_length=50 ,blank=False, default="")
    country = models.CharField(max_length=50 ,blank=False, default="")
    phone = models.CharField( max_length=50)
    state = models.CharField(max_length=50 ,blank=False, default="")
    total = models.DecimalField(max_digits=5, decimal_places=2)
    pyment_status = models.CharField(max_length=100,choices=PaymentStatus.choices,default=PaymentStatus.UNPAID)
    pyment_metod = models.CharField(max_length=100,choices=PaymentMethod.choices,default=PaymentMethod.COD)
    status = models.CharField(max_length=100,choices=OrderStatus.choices, default=OrderStatus.PROSSING)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
      return str(self.id)
    

# each order in The final order 
class OrderItem(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE,related_name='orderitems')
    name = models.CharField(max_length=100, blank=False, default="")
    quantity = models.IntegerField(default=0)
    price = models.DecimalField( max_digits=7, decimal_places=2, blank=False)

    def __str__(self):
      return self.name