# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


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


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_time = models.DateTimeField()

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


class Bgm(models.Model):
    bgm = models.TextField(blank=True, null=True)
    path = models.TextField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    objects = models.manager

    class Meta:
        managed = False
        db_table = 'bgm'


class Books(models.Model):
    path = models.TextField(db_collation='utf8mb4_unicode_ci', blank=True, null=True)
    book_id = models.IntegerField(blank=True, null=True)
    get_step = models.IntegerField(blank=True, null=True)
    page = models.IntegerField(blank=True, null=True)
    time = models.TextField(db_collation='utf8mb4_unicode_ci', blank=True, null=True)
    dir = models.TextField(db_collation='utf8mb4_unicode_ci', blank=True, null=True)
    name = models.TextField(db_collation='utf8mb4_unicode_ci', blank=True, null=True)
    task_id = models.TextField(db_collation='utf8mb4_unicode_ci', blank=True, null=True)
    man_uuid = models.TextField(db_collation='utf8mb4_unicode_ci', blank=True, null=True)
    objects = models.manager

    class Meta:
        managed = False
        db_table = 'books'


class SmallSay(models.Model):
    name = models.TextField(db_collation='utf8mb4_unicode_ci', blank=True, null=True)
    link = models.TextField(db_collation='utf8mb4_unicode_ci', blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)
    background_music = models.TextField(db_collation='utf8mb4_unicode_ci', blank=True, null=True)
    download_progress = models.IntegerField(blank=True, null=True)
    conversion_progress = models.IntegerField(blank=True, null=True)
    data = models.TextField(db_collation='utf8mb4_unicode_ci', blank=True, null=True)
    data2 = models.IntegerField(blank=True, null=True)
    data3 = models.FloatField(blank=True, null=True)
    conversion_max = models.IntegerField(blank=True, null=True)
    download_max = models.IntegerField(blank=True, null=True)
    data4 = models.DateTimeField(blank=True, null=True)
    time = models.TextField(db_collation='utf8mb4_unicode_ci', blank=True, null=True)
    add_back_progress = models.IntegerField(blank=True, null=True)
    add_back_max = models.IntegerField(blank=True, null=True)
    voice = models.TextField(db_collation='utf8mb4_unicode_ci', blank=True, null=True)
    background_music_id = models.IntegerField(blank=True, null=True)
    voice_id = models.IntegerField(blank=True, null=True)
    userid = models.IntegerField(blank=True, null=True)
    objects = models.manager

    class Meta:
        managed = False
        db_table = 'small_say'





class Voice(models.Model):
    name = models.TextField(blank=True, null=True)
    value = models.TextField(blank=True, null=True)
    msg = models.TextField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    objects = models.manager

    class Meta:
        managed = False
        db_table = 'voice'
