# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


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


class User(models.Model):
    name = models.TextField(blank=True, null=True)
    pass_field = models.TextField(db_column='pass', blank=True,
                                  null=True)  # Field renamed because it was a Python reserved word.
    logo = models.TextField(blank=True, null=True)
    objects = models.manager

    class Meta:
        managed = False
        db_table = 'user'


class Voice(models.Model):
    name = models.TextField(blank=True, null=True)
    value = models.TextField(blank=True, null=True)
    msg = models.TextField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    objects = models.manager

    class Meta:
        managed = False
        db_table = 'voice'
