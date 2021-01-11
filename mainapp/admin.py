from django.contrib import admin
from .models import Website, CafeMenu, Category, Product, Customer

# Register your models here.

admin.site.register(Website)
admin.site.register(CafeMenu)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Customer)
