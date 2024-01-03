from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        email = self.normalize_email(email).lower()
        if not email:
            raise ValueError( "email is a required field")
        user = self.model(email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_active') is not True:
            raise ValueError("Super user must be active") 
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Super user must be staff" )
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Super user must be superuser")
        
        return self.create_user(email, password, **extra_fields)




class User(AbstractBaseUser, PermissionsMixin):
    """""""
    email = models.EmailField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    
    