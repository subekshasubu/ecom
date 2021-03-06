from django.db import models
from django.urls import reverse

STATUS=(('In ', 'In Stock'),('Out','Out Of Stock'))
LABEL=(('New','New Product'),('Hot','Hot Products'),('sale','sale product'))
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length = 200)
    slug =  models.CharField(max_length= 200, unique=True)
    image = models.CharField(max_length= 200,blank=True)

    def __str__(self):
        return self.name
    def get_category_url(self):
        return reverse("home:category", kwargs={'slug': self.slug})


class Slider(models.Model):
    name = models.CharField(max_length=300)
    image = models.TextField()
    description = models.TextField()
    url = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Ad(models.Model):
    name = models.CharField(max_length=400)
    rank = models.IntegerField(unique=True)
    image = models.TextField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=300)
    rank = models.IntegerField()
    image = models.TextField()

    def __str__(self):
        return self.name

    def get_bran_url(self):
        return reverse('home:brand',kwargs={'name':self.name})

class Items(models.Model):
    name = models.CharField(max_length=300)
    price = models.IntegerField()
    slug = models.CharField(max_length=300,unique=True)
    discounted_price = models.IntegerField(default=0)
    description = models.TextField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    status = models.CharField(max_length=100,choices=STATUS)
    label = models.CharField(max_length=60,choices=LABEL,default='new')
    image = models.TextField(blank = True)
    def __str__(self):
        return self.name

    def get_url(self):
        return reverse("home:product",kwargs={'slug':self.slug})

    def get_cart_url(self):
        return reverse("home:add-to-cart", kwargs={'slug': self.slug})

class Cart(models.Model):
    item=models.ForeignKey(Items,on_delete=models.CASCADE)
    slug=models.CharField(max_length=300)
    quantity=models.IntegerField(default=1)
    user=models.CharField(max_length=200)
    date=models.DateTimeField(auto_now=True)
    total=models.IntegerField(null=True)

    def __str__(self):
        return self.user

    def delete_cart_url(self):
        return reverse("home:delete-cart", kwargs={'slug': self.slug})

    def delete_single_cart_url(self):
        return reverse("home:delete-single-cart", kwargs={'slug': self.slug})


class Contact(models.Model):
    name=models.CharField(max_length=300)
    email=models.CharField(max_length=500)
    subject=models.CharField(max_length=500)
    message=models.TextField()

    def __str__(self):
        return self.name
