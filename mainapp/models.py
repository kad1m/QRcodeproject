from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from django.urls import reverse
from django.contrib.auth.models import User


class Currency(models.Model):
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=10)

    def __str__(self):
        return str(self.symbol)


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    qr_code = models.ImageField(upload_to='qr_code', blank=True)
    menu_pdf = models.FileField(upload_to='menu', blank=True)
    stripeCustomerId = models.CharField(max_length=255, blank=True)
    stripeSubscriptionId = models.CharField(max_length=255, blank=True)
    profile_image = models.ImageField(upload_to='profile', blank=True)
    currency_symbol = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return str(self.company_name)

    def get_absolute_url(self):
        return reverse('second_page', kwargs={'id': self.id})

class CafeMenu(models.Model):
    name = models.CharField(max_length=255)
    qr_code = models.ImageField(upload_to='qr_code', blank=True)
    menu_pdf = models.FileField(upload_to='menu', blank=True)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('second_page', kwargs={'slug': self.name})


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    owner = models.ForeignKey(Customer, related_name='category_owner', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    product_image = models.ImageField(upload_to='product_image', blank=True)
    owner = models.ForeignKey(Customer, related_name='product_owner', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Website(models.Model):
    name = models.CharField(max_length=250)
    qr_code = models.ImageField(upload_to='qr_code', blank=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        qrcode_image = qrcode.make(self.name)
        canvas = Image.new('RGB', (qrcode_image.pixel_size, qrcode_image.pixel_size), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_image)
        fname = f'qr_code-{self.name}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)
