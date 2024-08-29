from django.urls import path ,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'products', views.ProductViewSet)

urlpatterns = [
  path('products_list/', views.get_all_products, name='products' ),
  path('', include(router.urls)),  
  path('products/new/', views.new_product,name='new_products'),
  path('products/<str:pk>/reviews/', views.create_review, name='create_review' ),
  path('products/<str:pk>/reviews/delete', views.delete_review, name='create_review' ),
]



handler404 = 'utils.error_view.handler404'
handler500 = 'utils.error_view.handler500'

