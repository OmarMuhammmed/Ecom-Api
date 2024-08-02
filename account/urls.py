from django.urls import path 
from . import views


urlpatterns =[
  path('signup/', views.signup, name='signup' ),
  path('current_user/', views.current_user, name='current_user'),
  path('current_user/update/', views.update_user, name='update_user'),
  path('forgot_password/', views.forgot_password, name='forgot_password'),
  path('reset_password/<str:token>', views.reset_password, name='reset_password'),

]