from django.db import models

class Category(models.Model):
    name=models.CharField(max_length=30)
    image=models.ImageField(upload_to="categories")
    description=models.TextField()
    def __str__(self):   #to implement print() function in class
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    image = models.ImageField(upload_to="products")
    price=models.IntegerField()
    stock=models.IntegerField()
    available=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)#only once
    updated=models.DateTimeField(auto_now=True)#changes every tima we update the record
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="products")

    def __str__(self):
        return self.name