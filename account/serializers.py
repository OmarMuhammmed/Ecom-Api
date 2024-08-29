from rest_framework import serializers
from .models import CustomUser as User
from django.contrib.auth.hashers import make_password

class SingUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name','last_name', 'user_name', 'email', 'password')
        
        extra_kwargs = {
            'first_name': {'required':True ,'allow_blank':False},
            'last_name' : {'required':True ,'allow_blank':False},
            'email' : {'required':False ,'allow_blank':False},
            'user_name' : {'required':False ,'allow_blank':False},
            'password' : {'required':True ,'allow_blank':False,'min_length':8}
        }
   
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email already exists!")
        return value

   
    def validate_user_name(self, value):
        if User.objects.filter(user_name=value).exists():
            raise serializers.ValidationError("This username is already taken!")
        return value

    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(SingUpSerializer, self).create(validated_data)    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name','last_name', 'user_name','password') 