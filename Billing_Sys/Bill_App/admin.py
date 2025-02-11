from django.contrib import admin
from .models import Product,Denomination,Purchase

# Register your models properly
admin.site.register(Product)
admin.site.register(Denomination)
admin.site.register(Purchase)
