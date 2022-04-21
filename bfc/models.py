from email.policy import default
from pickle import FALSE
from tokenize import blank_re
from django.db import models
from account.models import Registration
from django.utils import timezone
from django_resized import ResizedImageField
from PIL import Image
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from django.shortcuts import reverse
from django.urls import reverse, NoReverseMatch
import string
import random
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from model_utils import Choices
from django.utils.translation import ugettext_lazy as _
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill
from django.utils import timezone
import datetime
import os
from .utils import slugify_instance_title
import contextlib
from django.contrib.sitemaps import ping_google
from random import randint

# Create your models here.

"""
  def save(self, *args, **kwargs):
    if Post.objects.filter(title=self.title).exists():
      extra = str(randint(1, 10000))
      self.slug = slugify(self.title) + "_" + extra
    else:
      self.slug = slugify(self.title)
    super(Post, self).save(*args, **kwargs)
"""

PLAYER = Choices(
                ('GOALKEEPER', _('GOALKEEPER')),
                ('DEFENDER', _('DEFENDER')),
                ('MIDFIELDER', _('MIDFIELDER')),
                ('STRIKER', _('STRIKER')),
                ('LOAN', _('LOAN')),
)




def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))


class Post(models.Model):
  author = models.ForeignKey(Registration, on_delete=models.CASCADE,related_name='up_post')
  title = models.CharField(max_length=70, null=False)
  intro = models.TextField(max_length=200, null=True, blank=True, help_text='Please type the begining of the sentence here not more than 200 words')
  publish = models.DateTimeField(default=timezone.now)
  created = models.DateField(auto_now=True)
  updated = models.DateTimeField(auto_now_add=True)
  body = models.TextField()
  approve_to_post = models.BooleanField(default=False)
  postImage = ResizedImageField(size=[850, 510],crop=['middle', 'center'], quality=100, upload_to='post/images/', blank=True, null=True)
  slug = models.SlugField(max_length=255, unique=True)

  tags = TaggableManager()

  def sizable(self):
    return self.body[:1000]+"..."

  def remaining(self):
    return self.body[1000:]
  
  class Meta:
    ordering = ['-publish',]
    verbose_name_plural = _('Post')


  def __str__(self):
    return self.title


  def get_absolute_url(self):
    try:
        return reverse('bfc:news-details', kwargs={'slug': self.slug})
    except NoReverseMatch:
        return ""



class CurrentUpdate(models.Model):
  title = models.CharField(max_length=70, null=False, blank=False)
  image = ResizedImageField(size=[850, 510],crop=['middle', 'center'], quality=100, upload_to='current-update/images/',keep_meta=False, blank=True, null=True)
  slug = models.SlugField(max_length=255, unique=True)
  dateTime = models.DateTimeField(auto_now_add=True)
  intro = models.TextField(max_length=200, null=True, blank=True, help_text='Please type the begining of the sentence here not more than 200 words')
  body = models.TextField(null=True, blank=True)

  tags = TaggableManager()

  def __str__(self):
    return self.title

  def sizable(self):
    return self.body[:1000]+"..."

  def remaining(self):
    return self.body[1000:]

  class Meta:
    ordering = ['-dateTime']
    verbose_name_plural = _('CurrentUpdate')

  def get_absolute_url(self):
    try:
      return reverse('bfc:update-details', kwargs={'slug': self.slug})
    except NoReverseMatch:
      return ""



def upload_to_matches(instance, filename):
  now = timezone.now()
  base, extension = os.path.splitext(filename)
  extension = extension.lower()
  return f"Matches/{now:%y/%m}/{instance.pk}{extension}"

class Match(models.Model):
  homeTeam = models.CharField(max_length=250, null=False)
  awayTeam = models.CharField(max_length=250, null=False)
  scoreline_home = models.IntegerField(null=True, blank=True)
  scoreline_away = models.IntegerField(null=True, blank=True)
  hometeamLogo = models.ImageField(_('Picture'),upload_to=upload_to_matches)
  homeL = ImageSpecField(
      source='hometeamLogo',
      processors=[ResizeToFill(100, 100)],
      format='PNG',
      options={'quality': 100},
  )
  awayteamLogo = models.ImageField(upload_to='team-logo')
  awayL = ImageSpecField(
      source='awayteamLogo',
      processors=[ResizeToFill(100, 100)],
      format='PNG',
      options={'quality': 100},
  )
  awayteamLogo = models.ImageField(upload_to='team-logo')
  home_sm = ImageSpecField(
      source='awayteamLogo',
      processors=[ResizeToFill(50, 50)],
      format='PNG',
      options={'quality': 100},
  )
  awayteamLogo = models.ImageField(upload_to='team-logo')
  away_sm = ImageSpecField(
      source='awayteamLogo',
      processors=[ResizeToFill(50, 50)],
      format='PNG',
      options={'quality': 100},
  )
  tournamentLogo = models.ImageField(upload_to='tournament-logo')
  tournamentLogo_lg = ImageSpecField(
      source='tournamentLogo',
      processors=[ResizeToFill(140, 60)],
      format='PNG',
      options={'quality': 100},
  )
  tournamentLogo_sm = ImageSpecField(
      source='tournamentLogo',
      processors=[ResizeToFill(70, 30)],
      format='PNG',
      options={'quality': 100},
  )
  fixture_date_and_time = models.DateTimeField(null=False, blank=False, help_text='format: Date/Time(eg. sun')
  created = models.DateField(auto_now_add=True)
  slug = models.SlugField(max_length=250,null=False, unique=True)

  def delete(self, *args, **kwargs):
    from django.core.files.storage import default_storage
    
    if self.hometeamLogo:
      with contextlib.suppress(FileNotFoundError):
        default_storage.delete(self.homeL.path)
      self.hometeamLogo.delete()
    super().delete(*args, **kwargs)

    if self.awayteamLogo:
      with contextlib.suppress(FileNotFoundError):
        default_storage.delete(self.awayL.path)
      self.awayteamLogo.delete()
    super().delete(*args, **kwargs)


  class Meta:
    ordering = ['-fixture_date_and_time']
    verbose_name_plural = _('Match')

  def __str__(self):
    return self.homeTeam




def upload_to_banner(instance, filename):
  now = timezone.now()
  base, extension = os.path.splitext(filename)
  extension = extension.lower()
  return f"Banner/{now:%y/%m}/{instance.pk}{extension}"

class Banner(models.Model):
    playerBanner = models.ImageField(_('Picture'),upload_to=upload_to_banner)
    banner_xl = ImageSpecField(
      source='playerBanner',
      processors=[ResizeToFill(977, 488)],
      format='JPEG',
      options={'quality': 100},
    )
    banner_sm = ImageSpecField(
      source='playerBanner',
      processors=[ResizeToFill(499, 249)],
      format='JPEG',
      options={'quality': 100},
    )

    class Meta:
      verbose_name_plural = _('Banner')


def upload_to_player_profile(instance, filename):
  now = timezone.now()
  base, extension = os.path.splitext(filename)
  extension = extension.lower()
  return f"Player_Profile/{now:%y/%m}/{instance.pk}{extension}"

class PlayerProfile(models.Model):
  firstName = models.CharField(max_length=200, db_index=True)
  surname = models.CharField(max_length=200)
  position = models.CharField(choices=PLAYER, default='CHOOSE', max_length=30)
  nationality = models.CharField(max_length=30)
  place_birth = models.CharField(max_length=30)
  dob = models.DateField()
  jerseyNumber = models.IntegerField(null=FALSE, blank=False)
  year_signed = models.DateField(null=False, blank=False)
  appearance = models.CharField(max_length=5,null=False, blank=False,default='N/A')
  goals = models.CharField(max_length=5, null=False, blank=False,default='N/A')
  playerProfileImage = models.ImageField(_('Picture'), upload_to=upload_to_player_profile, blank=False, null=False)
  playerProfileImage_desktop1 = ImageSpecField(
    source='playerProfileImage',
    processors=[ResizeToFill(1300, 600)],
    format='JPEG',
    options={"quality": 100},
  )
  playerProfile = ImageSpecField(
    source='playerProfileImage',
    processors=[ResizeToFill(263, 263)], 
    format='JPEG',
    options={"quality": 100},
  )
  playerbanner_xl = ImageSpecField(
    source='playerProfileImage',
    processors=[ResizeToFill(977, 488)], 
    format='JPEG',
    options={"quality": 100},
  )
  playerbanner_sm = ImageSpecField(
    source='playerProfileImage',
    processors=[ResizeToFill(499, 249)], 
    format='JPEG',
    options={"quality": 100},
  )
  playerProfileImage_desktop2 = ImageSpecField(
    source='playerProfileImage',
    processors=[ResizeToFill(999, 461)],
    format='JPEG',
    options={"quality": 100},
  )
  playerProfileImage_desktop3 = ImageSpecField(
    source='playerProfileImage',
    processors=[ResizeToFill(700, 323)],
    format='JPEG',
    options={"quality": 100},
  )
  playerProfileImage_mobile = ImageSpecField(
    source='playerProfileImage',
    processors=[ResizeToFill(310, 120)],
    format='JPEG',
    options={"quality": 100},
  )

  slug = models.SlugField(max_length=200,null=False, unique=True)
  playerBio = models.TextField(null=True, blank=True, default='N/A')

  class Meta:
    ordering = ('firstName',)
    verbose_name_plural = _('PlayerProfile')

  def __str__(self):
    return self.firstName

  def get_absolute_url(self):
    try:
        return reverse('bfc:player-profile', kwargs={'slug': self.slug})
    except NoReverseMatch:
      return ""
      

  def delete(self, *args, **kwargs):
    from django.core.files.storage import default_storage
    
    if self.playerProfileImage:
      with contextlib.suppress(FileNotFoundError):
        default_storage.delete(self.playerProfileImage_desktop1.path)
        default_storage.delete(self.playerProfileImage_desktop2.path)
        default_storage.delete(self.playerProfileImage_desktop3.path)
        default_storage.delete(self.playerProfileImage_mobile.path)
      self.playerProfileImage.delete()
    super().delete(*args, **kwargs)



def upload_to_staff(instance, filename):
  now = timezone.now()
  base, extension = os.path.splitext(filename)
  extension = extension.lower()
  return f"Staff/{now:%y/%m}/{instance.pk}{extension}"

class Staff(models.Model):
  surName = models.CharField(max_length=100)
  firstName = models.CharField(max_length=100)
  position = models.CharField(max_length=100)
  staffBio = models.TextField(null=True, blank=True,default='N/A')
  slug = models.SlugField(max_length=200, null=False, blank=False, unique=True)
  profile_image = models.ImageField(_('Picture'), upload_to=upload_to_staff, blank=True, null=True)
  created = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ('-created',)
    verbose_name_plural = _('Staff')

  def __str__(self):
    return self.surName

  def get_absolute_url(self):
    return reverse('bfc:staff-profile', kwargs={'slug': self.slug})

  playerProfileImage_desktop1 = ImageSpecField(
    source='profile_image',
    processors=[ResizeToFill(1300, 600)],
    format='JPEG',
    options={"quality": 100},
  )
  playerProfile = ImageSpecField(
    source='profile_image',
    processors=[ResizeToFill(263, 263)], 
    format='JPEG',
    options={"quality": 100},
  )
  playerbanner_xl = ImageSpecField(
    source='profile_image',
    processors=[ResizeToFill(977, 488)], 
    format='JPEG',
    options={"quality": 100},
  )
  playerbanner_sm = ImageSpecField(
    source='profile_image',
    processors=[ResizeToFill(500, 450)], 
    format='JPEG',
    options={"quality": 100},
  )
  playerProfileImage_desktop2 = ImageSpecField(
    source='profile_image',
    processors=[ResizeToFill(999, 461)],
    format='JPEG',
    options={"quality": 100},
  )
  playerProfileImage_desktop3 = ImageSpecField(
    source='profile_image',
    processors=[ResizeToFill(700, 323)],
    format='JPEG',
    options={"quality": 100},
  )
  playerProfileImage_mobile = ImageSpecField(
    source='profile_image',
    processors=[ResizeToFill(310, 120)],
    format='JPEG',
    options={"quality": 100},
  )
  def delete(self, *args, **kwargs):
    from django.core.files.storage import default_storage
    
    if self.profile_image:
      with contextlib.suppress(FileNotFoundError):
        default_storage.delete(self.playerProfileImage_desktop1.path)
        default_storage.delete(self.playerProfileImage_desktop2.path)
        default_storage.delete(self.playerProfileImage_desktop3.path)
        default_storage.delete(self.playerProfileImage_mobile.path)
      self.profile_image.delete()
    super().delete(*args, **kwargs)


def upload_to_first_team_staff(instance, filename):
  now = timezone.now()
  base, extension = os.path.splitext(filename)
  extension = extension.lower()
  return f"First_Team_Staff/{now:%y/%m}/{instance.pk}{extension}"

class FirstTeamStaff(models.Model):
  first_Name = models.CharField(max_length=30, null=True, blank=True)
  last_Name = models.CharField(max_length=30, null=True, blank=True)
  role = models.CharField(max_length=30, null=True, blank=True)
  year_joined = models.DateField(null=True, blank=True)
  bio = models.TextField(default='N/A')
  created = models.DateTimeField(auto_now_add=True)
  staff_image = models.ImageField(_('Picture'), upload_to=upload_to_first_team_staff, blank=True, null=True)
  slug = models.SlugField(unique=True)

  team_staff_ProfileImage_desktop1 = ImageSpecField(
  source='staff_image',
  processors=[ResizeToFill(1300, 600)],
  format='JPEG',
  options={"quality": 100},
  )
  team_staff_ProfileImage_mobile = ImageSpecField(
  source='staff_image',
  processors=[ResizeToFill(310, 120)],
  format='JPEG',
  options={"quality": 100},
  )
  team_staff_ProfileImage_desktop2 = ImageSpecField(
  source='staff_image',
  processors=[ResizeToFill(999, 461)],
  format='JPEG',
  options={"quality": 100},
  )
  def delete(self, *args, **kwargs):
    from django.core.files.storage import default_storage
    
    if self.staff_image:
      with contextlib.suppress(FileNotFoundError):
        default_storage.delete(self.team_staff_ProfileImage_desktop1.path)
        default_storage.delete(self.team_staff_ProfileImage_desktop2.path)
        default_storage.delete(self.team_staff_ProfileImage_mobile.path)
      self.staff_image.delete()
    super().delete(*args, **kwargs)

  class Meta:
    verbose_name_plural = _('FirstTeamStaff')

  def get_absolute_url(self):
    return reverse('bfc:team-staff', kwargs={'slug': self.slug})

