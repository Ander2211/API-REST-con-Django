from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer


class ProductListAPIView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        name = self.request.GET.get('name')
        barcode = self.request.GET.get('barcode')
        if name:
            # búsqueda aproximada: coincidencia parcial, case-insensitive
            queryset = queryset.filter(nombre__icontains=name)
        if barcode:
            queryset = queryset.filter(codigo_barra=barcode)
        return queryset
