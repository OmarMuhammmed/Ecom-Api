from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import * 
from rest_framework import status
from rest_framework.response import Response
from .serializers import OrderItemSerializer,OrderSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.decorators import permission_classes
from product.models import Product
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework.views import APIView
from cart.models import CartItem
# Create your views here.
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class OrderApiView(APIView):
    permission_classes = [IsAuthenticated] 
    def get(self, request):
        queryset = Order.objects.all()
        serializer = OrderSerializer(queryset,many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = OrderSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    



class ManageOrder(APIView):
    # permission_classes =[IsAuthenticated]
    def get(self, request, pk ) :
        order_cache = cache.get(pk)
        if order_cache :
            order = order_cache
        else :   
            order = get_object_or_404(Order, pk=pk)
            cache.set(pk, order, CACHE_TTL)
        serilzer = OrderSerializer(order,many=False)
        return Response({'order' : serilzer.data})
    
    def put(self, request, pk, format=None):
        order = get_object_or_404(Order, pk=pk)
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, ):
        order = get_object_or_404(Order, pk=pk)
        order.delete()    
        return Response(status=status.HTTP_204_NO_CONTENT)     
    
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated,IsAdminUser])
def process_order(request,pk):
    order =get_object_or_404(Order, id=pk)
    order.status = request.data['status']
    order.save()
     
    serializer = OrderSerializer(order,many=False)
    return Response({'order':serializer.data})



@permission_classes([IsAuthenticated])
@api_view(['POST'])
def create_order(request):
    user = request.user
    data = request.data
    order_itmes = data['order_itmes'] 

    # If user  sent empty order 
    if order_itmes and len(order_itmes) == 0:
        return Response({'error': 'No order recieved'},status=status.HTTP_400_BAD_REQUEST)
    # Calculate total
    total = sum(item['price']*item['quantity'] for item in order_itmes )

    order = Order.objects.create(
        user = user,
        city = data['city'],
        zip_code = data['zip_code'],
        street = data['street'],
        phone = data['phone'],
        country = data['country'],
        total = total,
    )
    for i in order_itmes:
        product = Product.objects.get(id=i['product'])
        item = OrderItem.objects.create(
            product= product,
            order = order,
            name = product.name,
            quantity = i['quantity'],
            price = i['price']
        )
        product.stock -= item.quantity
        product.save()
        serializer = OrderSerializer(order,many=False)
        return Response(serializer.data)