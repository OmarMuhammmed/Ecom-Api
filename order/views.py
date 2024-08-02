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

# Create your views here.

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_orders(request):
  orders = Order.objects.all()
  serilzer = OrderSerializer(orders,many=True)
  return Response({
    'orders':serilzer.data
  })

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_order(request,pk):
  order = get_object_or_404(Order,pk=pk)
  serilzer = OrderSerializer(order,many=False)
  return Response({
    'order' : serilzer.data
  })


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_order(request,pk):
    order = get_object_or_404(Order, pk=pk) 
    order.delete()
    return Response({'details': "order is deleted"})



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