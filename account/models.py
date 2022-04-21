from email.policy import default
from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser,Group
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField
import uuid


GENDER_CHOICES = (
  ('M', 'Male'),
  ('F', 'Female'),
)

class Role(Group):
  class Meta:
    proxy = True
    verbose_name = _('Role')
    verbose_name_plural = _('Roles')

  def __str__(self):
    return self.name


class MyRegistrationManager(BaseUserManager):
  def create_user(self, username="", email="", password="", **extra_fields):
    if not email:
      raise ValueError('Users must have an email address')
    email = self.normalize_email(email)
    user = self.model(username=username, email=email,  **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user


  def create_superuser(self, username="", email="", password=""):
    user = self.create_user(email=email, password=password, username=username)
    user.is_superuser = True
    user.is_staff = True
    user.save(using=self._db)
    return user


class Registration(AbstractUser):
  uuid = models.UUIDField(primary_key=True, default=None, editable=False)
  email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
  contact = models.CharField(max_length=15,null=True, blank=True)
  username = models.CharField(max_length=150, editable=False)
  country = CountryField()
  dob = models.DateField(null=True, blank=True)
  gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='N/A')



  # notice the absence of a "Password field", that is built in.

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []

  objects = MyRegistrationManager()

  def save(self, *args, **kwargs):
    if self.pk is None:
      self.pk = uuid.uuid4()
    super().save(*args, **kwargs)

