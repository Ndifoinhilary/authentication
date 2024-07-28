from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,BaseUserManager




class usermanager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        email = self.normalize_email(email).lower()
        if  not email:
            raise ValueError(f'{email} is a required field')
        user = self.model(email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
