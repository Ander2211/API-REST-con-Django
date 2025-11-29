from django.urls import path
from .views import (
    ProductListCreateAPIView,
    ProductRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path('productos/', ProductListCreateAPIView.as_view(), name='product-list'),
    path('productos/<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name='product-detail'),
]
