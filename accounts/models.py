from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from ast import arg
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
# from django_countries.fields import CountryField
import uuid
from django.conf import settings



# Create your models here.
# --------------------
# SHARED MANAGERS
# --------------------

# class AllUserManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset()


class ActiveUserManager(models.Manager):
    """Return only active (not soft-deleted) users."""
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class AllUserManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db)

class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        for obj in self:
            obj.soft_delete()

class CustomPopUpAccountManager(BaseUserManager, ActiveUserManager):

    # def get_queryset(self):
    #     return super().get_queryset().filter(deleted_at__isnull=True)

    def get_by_natural_key(self, email):
        return self.get(email=email)

    def create_superuser(self, email, password=None, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must be assinged to is staff=True.'))

        if other_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must be assigned to is_superuser=True.'))

        return self.create_user(email, password=password, **other_fields)

    def create_user(self, email, password=None, **other_fields):
        if not email:
            raise ValueError(_('An email address is required.'))

        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

# --------------------
# SHARED USER MODEL
# --------------------
class User(AbstractBaseUser, PermissionsMixin):
    """Universal user model shared across all apps"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # universal identify fields
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)

    # universal phone / preference fields
    mobile_phone = models.CharField(max_length=20, blank=True, null=True)
    mobile_notification = models.BooleanField(default=True)

    last_password_reset = models.DateTimeField(null=True, blank=True)

    # status and timestamps
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CustomPopUpAccountManager()
    all_objects = AllUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    class Meta:
        db_table = 'shared_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'


    def soft_delete(self):
        self.is_active = False
        self.deleted_at = now()
        self.save()


    def delete(self, using=None, keep_parents=False):
        """Override delete() to perform a soft delete"""
        self.soft_delete()

    def restore(self):
        self.is_active = True
        self.deleted_at = None
        self.save()

    @property
    def is_deleted(self):
        return self.deleted_at is not None

    def hard_delete(self):
        """Permanently delete the account (only for admin use)."""
        super().delete()

    def __str__(self):
        return self.email
