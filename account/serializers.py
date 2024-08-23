from rest_framework import serializers
from .models import CustomUser as User


class SingUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name','last_name', 'email', 'password')
        
        extra_kwargs = {
            'first_name': {'required':True ,'allow_blank':False},
            'last_name' : {'required':True ,'allow_blank':False},
            'email' : {'required':False ,'allow_blank':False},
            'user_name' : {'required':False ,'allow_blank':False},
            'password' : {'required':True ,'allow_blank':False,'min_length':8}
        }

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name','last_name', 'user_name','password') 