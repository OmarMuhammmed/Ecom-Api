from django.urls import path ,include
from .views import CartViewSet, CartItemViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('cart', CartViewSet)
router.register('cart_item', CartItemViewSet)

urlpatterns = [
    path('', include(router.urls))
]
