from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# Create your models here.

class Organization(models.Model):
    name = models.CharField(max_length=100, unique=True)
    frontend_domain = models.CharField(max_length=255)
    backend_domain = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.name

# class User(AbstractUser):
#     organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    
#     # Add related_name to groups
#     groups = models.ManyToManyField(
#         Group,
#         related_name='custom_user_set',  # Custom related name
#         blank=True,
#         help_text='The groups this user belongs to.',
#         verbose_name='groups',
#         related_query_name='user',
#     )
    
#     # Add related_name to user_permissions
#     user_permissions = models.ManyToManyField(
#         Permission,
#         related_name='custom_user_permissions_set',  # Custom related name
#         blank=True,
#         help_text='Specific permissions for this user.',
#         verbose_name='user permissions',
#         related_query_name='user',
#     )

from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
class CustomUserManager(UserManager):
    def _create_user(self,username, password, **extra_fields):
        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username: str, password: str | None = ..., **extra_fields: Any) -> Any:
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)
    
    def create_superuser(self, username: str, password: str | None, **extra_fields: Any) -> Any:
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(username, password, **extra_fields)
    


class User(AbstractBaseUser, PermissionsMixin):
    #email = models.EmailField(unique=True, null=True, blank=True)
    username = models.CharField(max_length=150, unique=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=150, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True, null=True)
    
    USER_TYPE_CHOICES = [
        ('editor', 'Editor'),
        ('viewer', 'Viewer'),
    ]
    TYPE_SCREEN = 'viewer'
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='viewer')
    credential_sent = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'username'
    #EMAIL_FIELD = 'email'
    #REQUIRED_FIELDS = ['email']
    
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        
    def get_full_name(self):
        return self.username
    def short_name(self):
        return self.username
    


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)