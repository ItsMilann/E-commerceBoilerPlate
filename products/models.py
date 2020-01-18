from django.db import models
from django.shortcuts import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField


CATEGORY_CHOICES = (
    ('men', 'men'),
    ('women', 'women'),
    ('kids', 'kids')
)
FEATURE_CHOICES = (
    ('trending', 'trending'),
    ('featured', 'featured'),
    ('collection', 'collection')
)
LABEL_CHOICES = (
    ('New', 'New'),
    ('Best Seller', 'Best Seller'),
    ('Suggested', 'Suggested')
)

COLOR_LABEL = (
    ('primary', 'primary'),
    ('secondary', 'secondary'),
    ('danger', 'danger')
    
)
class Product(models.Model):
    name = models.CharField(max_length=50)
    picture = models.ImageField(upload_to= 'items/images', blank = True, null = True)
    price = models.IntegerField()
    discounted_price = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=250)
    additional_information = models.TextField(max_length=3000)
    category = models.CharField(choices = CATEGORY_CHOICES, max_length = 5)
    featured = models.CharField(choices = FEATURE_CHOICES, max_length = 10, blank=True, null=True)
    label = models.CharField(choices = LABEL_CHOICES, max_length = 15, blank=True, null=True)
    color_label = models.CharField(choices = COLOR_LABEL, max_length = 9, blank=True, null=True)
    slug = models.SlugField()

    def get_discount_percent(self):
        if self.discounted_price:
            discount_percent = ((self.price - self.discounted_price)/self.price)*100
            discount_percent = round(discount_percent, 2)
            return discount_percent

    def get_absolute_url(self, *args, **kwagrs):
        return reverse('product_detail', kwargs={'id':self.id})

    def get_add_cart_url(self, *args, **kwagrs):
        return reverse('add_to_cart', kwargs={'id':self.id})

    def get_remove_cart_url(self, *args, **kwagrs):
        return reverse('remove_from_cart', kwargs={'id':self.id})

    def __str__(self):
        return self.name

class OrderProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField ( default=False )
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} of {self.product.name}.'
    
    def get_total_price(self):
        total_price = 0
        if self.product.discounted_price:
            total_price = self.quantity*self.product.discounted_price
        else:
            total_price = self.quantity*self.product.price
        return total_price


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    reference_code = models.CharField(max_length=20)
    product = models.ManyToManyField(OrderProduct)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(auto_now_add = True)
    billing_address = models.ForeignKey('BillingAddress', on_delete = models.SET_NULL, blank=True, null=True)
    payment_info = models.ForeignKey('Payment', on_delete = models.SET_NULL, blank=True, null=True)
    order_status = models.ForeignKey('OrderStatus', on_delete = models.SET_NULL, blank=True, null=True)


    def __str__(self):
        return self.user.username

    def get_grand_total(self):
        total = 0
        for product in self.product.all():
            total += product.get_total_price()
        return total
    
    def get_total_quantity(self):
        total = 0
        for product in self.product.all():
            total += product.quantity
        return total

class BillingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    country = CountryField()
    street_address = models.CharField(max_length = 100)
    appartment_address = models.CharField(max_length = 100)
    town = models.CharField(max_length = 100)
    zip_code = models.CharField(max_length = 100)

    def __str__(self):
        return f'Address'


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    payment_method = models.CharField(max_length=10)
    charge_id = models.CharField(max_length=50)
    amount = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Payment'

class OrderStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    pre_processing = models.BooleanField(default=False)
    being_delivered = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return f'Order Status'

class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete = models.CASCADE)
    message = models.TextField()
    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(blank=True, null = True)

    def __str__(self):
        return f'{self.accepted}'