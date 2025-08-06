from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("role", User.Roles.ADMIN)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class Roles(models.TextChoices):
        ADMIN        = 'ADMIN',        'Admin'
        DOCTOR       = 'DOCTOR',       'Doctor'
        RECEPTIONIST = 'RECEPTIONIST', 'Receptionist'
        PHARMACY     = 'PHARMACY',     'Pharmacy'
        LAB_TECH     = 'LAB_TECH',     'Lab Technician'
        ACCOUNTANT   = 'ACCOUNTANT',   'Accountant'
        INVENTORY    = 'INVENTORY',    'Inventory Manager'
        HR           = 'HR',           'HR Manager'

    email       = models.EmailField(unique=True)
    first_name  = models.CharField(max_length=30)
    last_name   = models.CharField(max_length=30)
    role        = models.CharField(max_length=20, choices=Roles.choices)
    is_active   = models.BooleanField(default=True)
    is_staff    = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role']

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"


class AuditLog(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    action     = models.CharField(max_length=50)
    path       = models.CharField(max_length=255, blank=True)
    method     = models.CharField(max_length=10, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp} - {self.user.email} - {self.action}"