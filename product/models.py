from django.db import models
from account.models import CustomUser as User
# Create your models here.

class Category(models.TextChoices):
    ELECTRONICS = 'Electronics' ,
    FOOD = 'food',
    KIDS = 'kids',
    HOME = 'home',
    CLOTHES = 'clothes', 

    def __str__(self):
        return 

    
class Product(models.Model):
    name = models.CharField(max_length=50,default="",blank=False)
    description = models.TextField(max_length=1000,default="",blank=False)
    price = models.DecimalField(max_digits=7,decimal_places=2,default=0)
    brand = models.CharField(max_length=50,default="",blank=False)
    category = models.CharField(max_length=40,choices=Category.choices)
    ratings = models.DecimalField(max_digits=3,decimal_places=2,default=0)
    stock = models.IntegerField(default=0)
    createAt = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name
    

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    rating = models.IntegerField(default=0)
    comment = models.TextField(max_length=1000)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product} taken {self.rating} from {self.user}"

    