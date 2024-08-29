from django.shortcuts import render
from rest_framework.decorators import api_view
from product.filters import ProductFilter 
from .models import * 
from rest_framework import status
from rest_framework.response import Response
from .serializers import ProductSerializer,ReviewSerializer
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.decorators import permission_classes
from django.db.models import Avg
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework import viewsets
# Create your views here.

# Get timeout from settings if exsists
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@api_view(['GET'])
def get_all_products(request):
    filiterset = ProductFilter(request.GET, queryset=Product.objects.all().order_by('id'))
    count = filiterset.qs.count()
    respage = 12 
    paginator = PageNumberPagination()
    paginator.page_size = respage
    queyrset =  paginator.paginate_queryset(filiterset.qs,request)
    serlizer =  ProductSerializer(queyrset,many=True) 
    return Response(
                    {
                     "products":serlizer.data,
                     "per page":respage, 
                     "count":count,
                     }
                     )

class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_product(request):
    serializer = ProductSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"product":serializer.data})
    else:
        return Response(serializer.errors)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request,pk):
    user = request.user
    product = get_object_or_404(Product,id=pk)
    data = request.data

    '''1- reviews in related_name in models 
       2- if user write rating to product or not '''
    review = product.reviews.filter(user=user) 
   
    if data['rating'] <= 0 or data['rating'] > 10:
        return Response({"error":'Please select between 1 to 5 only'}
                        ,status=status.HTTP_400_BAD_REQUEST) 
    
    elif review.exists():
        new_review = {
            'rating':data['rating'], 
            'comment':data['comment']
              }
        review.update(**new_review)
        # Calculate Avgerge ratings
        rating = product.reviews.aggregate(avg_ratings = Avg('rating'))
        product.ratings = rating['avg_ratings']
        product.save()

        return Response({'details':'Product review updated'})
    else:
        Review.objects.create(
            user=user,
            product=product,
            rating= data['rating'],
            comment= data['comment']
        )
        rating = product.reviews.aggregate(avg_ratings = Avg('rating'))
        product.ratings = rating['avg_ratings']
        product.save()
        return Response({'details':'Product review created'})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request,pk):
    user = request.user
    product = get_object_or_404(Product,id=pk)

    review = product.reviews.filter(user=user) 
    
    if review.exists():
        review.delete()
        rating = product.reviews.aggregate(avg_ratings = Avg('rating'))
        if rating['avg_ratings'] is None:
            rating['avg_ratings'] = 0
            product.ratings = rating['avg_ratings']
            product.save()
            return Response({'details':'Product review deleted'})
    else:
        return Response({'error':'Review not found'},status=status.HTTP_404_NOT_FOUND)

  