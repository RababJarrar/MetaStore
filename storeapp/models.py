from django.db import models

from login.models import Customer, Seller

from django.db import models


class Top_sellers(models.Model):
    seller = models.ForeignKey(Seller,
                               related_name='top_seller',
                               on_delete=models.CASCADE
                               )


class Product_category(models.Model):
    name = models.CharField(max_length=55)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)


class Product(models.Model):
    name = models.CharField(max_length=55)
    quantity = models.IntegerField()
    category = models.ForeignKey(
        Product_category, related_name='products', on_delete=models.CASCADE)
    description = models.TextField()
    price = models.FloatField()
    seller = models.ManyToManyField(
        Seller, related_name='product')
    sale = models.IntegerField(default=5)
    image = models.ImageField(null=True, blank=True, upload_to='media/')
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)


class Top_product(models.Model):
    products = models.ForeignKey(
        Product, related_name='top_product', on_delete=models.CASCADE)


class Order_item(models.Model):
    product = models.ForeignKey(
        Product, related_name='order_item', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)


class Order(models.Model):
    items = models.ManyToManyField(
        Order_item, related_name='cart', blank=True)
    total = models.FloatField()
    customer = models.ForeignKey(
        Customer, related_name='orders', on_delete=models.CASCADE)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)
