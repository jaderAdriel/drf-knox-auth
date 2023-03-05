from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from .validators import cpf_validator

class UserManager( BaseUserManager ):
    def create_user(self, cpf, password, **extra_fields):
        if not cpf:
            raise ValueError('the cpf was not given')
        
        user = self.model(cpf=cpf, **extra_fields)
        user.set_password(password)
        user.save()

        return user
    
    def create_superuser(self, cpf, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('superuser must have is_staff = True')

        if not extra_fields.get('is_staff'):
            raise ValueError('superuser must have is_superuser = True')

        return self.create_user(cpf, password, **extra_fields)

class User( AbstractBaseUser ):

    ROLE_CHOICES = (
        (1, 'Administrator'),
        (2, 'Caregiver'),
        (3, 'BabySitter'),
        (4, 'Client'),
    )
    GENDER_CHOICES = (
        (1, 'Male'),
        (2, 'Famale'),
        (3, 'Other'),
    )

    cpf = models.CharField( validators=[cpf_validator] ,max_length=11, unique=True )
    email = models.EmailField( blank=True, null=True, )
    name = models.CharField( max_length=70,blank=False, null=False )
    date_joined = models.DateTimeField( auto_now_add=True)
    role = models.PositiveSmallIntegerField( choices=ROLE_CHOICES, blank=False, null=False )
    gender = models.PositiveSmallIntegerField( choices=GENDER_CHOICES, blank=False, null=False )
    is_active = models.BooleanField( default=True )
    is_superuser = models.BooleanField( default=False )
    is_staff = models.BooleanField( default=False )

    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = ['email', 'name']

    objects = UserManager()

    def __str__(self):
        return self.name
    
    def has_module_perms(self, app_label):
        return True
    
    def has_perm(self, perm, obj=None):
        return True