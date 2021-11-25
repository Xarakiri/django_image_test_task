from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from .utils import get_file_path


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        """Создает и возвращает пользователя"""
        if username is None:
            raise TypeError('Users must have a username.')
        
        if email is None:
            raise TypeError('Users must have an email address.')
        
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user
    
    def create_superuser(self, username, email, password):
        """Создает и возвращает пользователя с привилегиями админа"""
        if password is None:
            raise TypeError('Superusers must have a password.')
        
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()
    
    def get_full_name(self):
        return self.username
    
    def get_short_name(self):
        return self.username
    
    def _generate_jwt_token(self):
        """
        Генерируем JWT, в котором хранится идентификатор этого
        пользователя, срок действия токена составляет 1 день от создания.
        """
        dt = datetime.now() + timedelta(days=1)
        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

        return token.decode('utf-8')


class Image(models.Model):
    image = models.ImageField(upload_to=get_file_path)

    def __str__(self) -> str:
        return self.title
