# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

from utils.models.mixins import BaseTimeModelMixin


# Create your models here.

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        return self._create_user(username, password, **extra_fields)


class User(BaseTimeModelMixin, AbstractBaseUser):
    '''
    用户
    '''
    user_id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=200)  # 邮箱
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=1024)
    department = models.CharField(max_length=200)
    objects = UserManager()

    @classmethod
    def create_or_update_users(cls, **kwargs):
        fields = {
            "username": kwargs.get("username"),
            "email": kwargs.get("email"),
            "department": kwargs.get("department"),
        }
        account = User.objects.filter(username=kwargs['username'])
        if account:
            account.update(**fields)
            return account[0].id
        else:
            raw_password = kwargs['password']
            account = cls(**fields)
            account.set_password(raw_password)
            account.save()
            return account.id

    class Meta:
        db_table = 'account_user'