from rest_framework.response import Response
from .serializers import CartSerializer, CartItemSerializer
from .models import Cart, CartItem 
from rest_framework import viewsets
# Create your views here.

class CartViewSet(viewsets.ModelViewSet):
    # auth 
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartItemViewSet(viewsets.ModelViewSet):
    # auth 
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


