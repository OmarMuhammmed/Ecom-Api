from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import CustomUser as User
from django.contrib.auth.hashers import make_password 
from rest_framework import status
from .serializers import SingUpSerializer,UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from project import settings
# Create your views here.


@api_view(['POST'])
def signup(request):
    serializer = SingUpSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {'details': 'Your account registered successfully!'},
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])  
@permission_classes([IsAuthenticated])
def current_user(request):
    user = UserSerializer(request.user,many=False)
    return Response(user.data)

 
@api_view(['PUT'])  
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user
    data = request.data 
    
    user.first_name = data['first_name'] 
    user.last_name = data['last_name'] 
    user.user_name = data['user_name'] 
    user.email = data['email'] 

    if data['password'] != '':
        user.password = make_password(data['password'])


    user.save()
    serializer = UserSerializer(user,many=False) 
                
    return Response(serializer.data)  


def get_current_host(request):
    protocol = request.is_secure() and 'https' or 'http' # protocol is secure or not 
    host = request.get_host()
    
    return "{protocol}://{host}/".format(protocol=protocol, host=host)


 
@api_view(['POST'])
def forgot_password(request):
   data = request.data 
   user = get_object_or_404(User,user_name=data['user_name'])

   # genarate a token 
   token = get_random_string(40)
   # set the token validity period to 30 minutes from now.
   expire_data = datetime.now() + timedelta(minutes=30)
   
   # save token,expire_data in profile 
   user.profile.reset_password_token = token # relatedname = 'profile'
   user.profile.reset_password_expire = expire_data
   user.profile.save()
   
   host = get_current_host(request)
   link = 'http://localhost:8000/api/reset_password/{token}'.format(token=token)
   message = 'Your password reset link is : {link}'.format(link=link)
   subject = "password resert from Ecom "
   send_mail(
       subject,
       message,
       settings.EMAIL_HOST_USER,
       [data['email']]
   )
   return Response({'details':'password reset sent to {email}'.format(email=data['email'])})


 
@api_view(['POST'])
def reset_password(request,token):
   data = request.data 
   user = get_object_or_404(User,profile__reset_password_token = token )

   if user.profile.reset_password_expire.replace(tzinfo=None) < datetime.now() :
      return Response({'Error':'Token is expire'},status=status.HTTP_400_BAD_REQUEST)

   if data['password'] != data['confirmpassword'] :
      return Response({'Error':'Password are not same'},status=status.HTTP_400_BAD_REQUEST)
    
   # Update password 
   user.password = make_password(data['password'])

   # Deleted becuse password is changed 
   user.profile.reset_password_token = ""
   user.profile.reset_password_expire = None
   
   user.profile.save()
   user.save()
   
  
   return Response({'details':'password reset Done '})




