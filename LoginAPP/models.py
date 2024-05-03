from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models

# Define un administrador personalizado para el modelo de usuario
class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('El nombre de usuario debe ser proporcionado')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')

        return self.create_user(username, password, **extra_fields)

# Define el modelo personalizado de usuario
class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)  # Define una clave primaria 'id'
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)  # Debes incluir un campo de contraseña

    # Define los campos de relación con un related_name personalizado
    groups = models.ManyToManyField(Group, blank=True, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='custom_user_set')

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    # Otros campos requeridos como 'email', 'nombre', etc., según tus necesidades

    def __str__(self):
        return self.username
