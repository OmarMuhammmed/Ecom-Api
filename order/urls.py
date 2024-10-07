from django.urls import path
from . import views

urlpatterns = [
   # List, Post Order
   path('orders/', views.OrderApiView.as_view(), name='get_all_orders' ),
   # Get , Put, Delete Order 
   path('orders/<int:pk>', views.ManageOrder.as_view(), name='manage_order' ),
   path('orders/new/', views.create_order, name='create_order' ),
   path('orders/process/<int:pk>', views.process_order, name='delete_order' ),
]