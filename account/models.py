from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, first_name, last_name , user_name, email=None,  password=None,**extra_fields):
        # Vaildation 
        if not user_name:
            raise ValueError('The username field must be set')
       
        user = self.model(
                            email = self.normalize_email(email),
                            user_name = user_name,
                            first_name = first_name,
                            last_name = last_name,
                            **extra_fields 
                         )
        user.set_password(password),
        user.save(using=self._db)
        return user

    
    def create_superuser(self,user_name, email=None, password=None, **extra_fields):
        
        # Create the user with the provided parameters
        user = self.create_user(
            first_name='Admin',
            last_name='User',
            user_name=user_name,
            email=self.normalize_email(email),
            password=password,
            **extra_fields
        )
        # Set default permissions for superuser
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        # Set the password and save the user
        user.set_password(password)
        user.save(using=self._db)
        return user



class CustomUser(AbstractBaseUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    user_name = models.CharField(max_length=50, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'user_name' # to login django dash 

    objects = CustomUserManager()
    
    class Meta:
        verbose_name_plural = 'Users'
    

    def __str__(self):
        return self.user_name

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, related_name='profile',on_delete= models.CASCADE)
    reset_password_token = models.CharField(max_length=50,default="",blank=True)
    reset_password_expire = models.DateTimeField(blank=True,null=True)

    @receiver(post_save, sender=CustomUser)
    def save_profile(sender,instance,created, **kwargs):
        user = instance
        if created :
            profile = Profile(user=user)
            profile.save()
