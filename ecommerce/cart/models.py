from django.db import models
from django.db import models
from shop.models import Product
from django.contrib.auth.models import User
# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    date_added = models.DateTimeField(auto_now_add=True)


    def subtotal(self): #Self means current cart object
           return self.product.price*self.quantity

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=20,blank=True)
    amount=models.IntegerField()
    address = models.TextField()
    payment_method = models.CharField(max_length=30)
    phone=models.IntegerField()
    ordered_date = models.DateTimeField(auto_now_add=True)
    is_ordered = models.BooleanField(default=False)
    delivery_status=models.CharField(max_length=20,default="Pending")

    def __str__(self):
        return self.order_id


class Order_items(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name="products")
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()

    def __str__(self):
        return self.order.order_id
