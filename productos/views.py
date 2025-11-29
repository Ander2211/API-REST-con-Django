from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer


class ProductListCreateAPIView(ListCreateAPIView):
    """Soporta GET (lista + filtros) y POST (crear producto).

    Filtros de consulta:
    - name: búsqueda parcial sobre `nombre` (icontains)
    - barcode: coincidencia exacta sobre `codigo_barra`
    """
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        name = self.request.GET.get('name')
        barcode = self.request.GET.get('barcode')
        if name:
            queryset = queryset.filter(nombre__icontains=name)
        if barcode:
            queryset = queryset.filter(codigo_barra=barcode)
        return queryset


class ProductRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """Soporta GET/PUT/PATCH/DELETE sobre `/api/productos/<pk>/`."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
