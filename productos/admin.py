from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'codigo_barra', 'precio', 'stock')
    search_fields = ('nombre', 'codigo_barra')
