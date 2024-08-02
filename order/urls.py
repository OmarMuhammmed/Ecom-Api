from django.urls import path
from . import views

urlpatterns = [
   path('orders/', views.get_orders, name='get_all_orders' ),
   path('orders/<int:pk>', views.get_order, name='get_order' ),
   path('orders/new/', views.create_order, name='create_order' ),
   path('orders/process/<int:pk>', views.process_order, name='delete_order' ),
   path('orders/delete/<int:pk>', views.delete_order, name='delete_order' ),
]