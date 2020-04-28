from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.


class MyUserManager(BaseUserManager):
    """ custom user manager for user model """

    def create_user(self, email, username, adhar_id, password=None):
        """ create user """
        if not email:
            raise ValueError("user must have email ")

        user = self.model(
                email = self.normalize_email(email),
                username = username,
                adhar_id=adhar_id
                )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, adhar_id, password=None):
        """ create superuser """

        user = self.create_user(email, username, adhar_id, password=password)
        user.is_admin=True
        user.is_staff=True

        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    """ overriding default django user model """

    email = models.EmailField(max_length=255, unique=True)
    adhar_id = models.IntegerField(unique=True)
    username = models.CharField(max_length=255)

    is_active=models.BooleanField(default=True)
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD='adhar_id'
    REQUIRED_FIELDS=['email', 'username']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """ user have specific permission """
        return True

    def has_module_perms(self, app_label):
        """ user have permission to view app """
        return True



