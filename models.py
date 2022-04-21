# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AccountRegistration(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    email = models.CharField(unique=True, max_length=255)
    contact = models.IntegerField(blank=True, null=True)
    firstname = models.CharField(db_column='firstName', max_length=30)  # Field name made lowercase.
    surname = models.CharField(db_column='surName', max_length=200, blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(max_length=100, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    date_joined = models.DateTimeField()
    is_active = models.BooleanField()
    is_admin = models.BooleanField()
    is_staff = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'account_registration'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class BfcBanner(models.Model):
    playerbanner = models.CharField(db_column='playerBanner', max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bfc_banner'


class BfcCurrentupdate(models.Model):
    title = models.CharField(max_length=70)
    image = models.CharField(max_length=100, blank=True, null=True)
    slug = models.CharField(unique=True, max_length=255)
    datetime = models.DateTimeField(db_column='dateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bfc_currentupdate'


class BfcMatch(models.Model):
    hometeam = models.CharField(db_column='homeTeam', max_length=250)  # Field name made lowercase.
    awayteam = models.CharField(db_column='awayTeam', max_length=250)  # Field name made lowercase.
    scoreline_home = models.IntegerField(blank=True, null=True)
    scoreline_away = models.IntegerField(blank=True, null=True)
    hometeamlogo = models.CharField(db_column='hometeamLogo', max_length=100)  # Field name made lowercase.
    awayteamlogo = models.CharField(db_column='awayteamLogo', max_length=100)  # Field name made lowercase.
    tournamentlogo = models.CharField(db_column='tournamentLogo', max_length=100)  # Field name made lowercase.
    fixture_date_and_time = models.DateTimeField()
    created = models.DateTimeField()
    slug = models.CharField(unique=True, max_length=250)

    class Meta:
        managed = False
        db_table = 'bfc_match'


class BfcPlayerprofile(models.Model):
    firstname = models.CharField(db_column='firstName', max_length=200)  # Field name made lowercase.
    surname = models.CharField(max_length=200)
    position = models.CharField(max_length=30)
    nationality = models.CharField(max_length=30)
    dob = models.DateField()
    positionnumber = models.IntegerField(db_column='positionNumber', blank=True, null=True)  # Field name made lowercase.
    playerprofileimage = models.CharField(db_column='playerProfileImage', max_length=100, blank=True, null=True)  # Field name made lowercase.
    slug = models.CharField(unique=True, max_length=200)
    playerbio = models.TextField(db_column='playerBio', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bfc_playerprofile'


class BfcPost(models.Model):
    title = models.CharField(max_length=70)
    synopsis = models.TextField()
    publish = models.DateTimeField()
    created = models.DateField()
    updated = models.DateTimeField()
    body = models.TextField()
    postimage = models.CharField(db_column='postImage', max_length=100, blank=True, null=True)  # Field name made lowercase.
    slug = models.CharField(unique=True, max_length=255)
    author = models.ForeignKey(AccountRegistration, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'bfc_post'


class BfcProfile(models.Model):
    firstname = models.CharField(db_column='firstName', max_length=200)  # Field name made lowercase.
    surname = models.CharField(max_length=200)
    position = models.CharField(max_length=30)
    nationality = models.CharField(max_length=30)
    dob = models.DateField()
    positionnumber = models.IntegerField(db_column='positionNumber', blank=True, null=True)  # Field name made lowercase.
    playerprofileimage = models.CharField(db_column='playerProfileImage', max_length=100)  # Field name made lowercase.
    slug = models.CharField(unique=True, max_length=200)
    playerbio = models.TextField(db_column='playerBio', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bfc_profile'


class BfcStaff(models.Model):
    surname = models.CharField(db_column='surName', max_length=100)  # Field name made lowercase.
    firstname = models.CharField(db_column='firstName', max_length=100)  # Field name made lowercase.
    position = models.CharField(max_length=100)
    staffbio = models.TextField(db_column='staffBio', blank=True, null=True)  # Field name made lowercase.
    slug = models.CharField(unique=True, max_length=200)
    profile_image = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'bfc_staff'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AccountRegistration, models.DO_NOTHING)
    action_flag = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DjangoSite(models.Model):
    name = models.CharField(max_length=50)
    domain = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'django_site'


class TaggitTag(models.Model):
    name = models.CharField(unique=True, max_length=100)
    slug = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'taggit_tag'


class TaggitTaggeditem(models.Model):
    object_id = models.IntegerField()
    content_type = models.ForeignKey(DjangoContentType, models.DO_NOTHING)
    tag = models.ForeignKey(TaggitTag, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'taggit_taggeditem'
        unique_together = (('content_type', 'object_id', 'tag'),)
