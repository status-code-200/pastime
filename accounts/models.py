from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomizedUserManager(BaseUserManager):
    def create_user(self, username, email, password, date_of_birth=None):
        if not email or username or password:
            raise ValueError('Not all required fields was filled')

        user = self.model(
                username=username,
                email=self.normalize_email(email),
                date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        if not email or not username or not password:
            raise ValueError('Not all required fields was filled')

        user = self.model(
                username=username,
                email=self.normalize_email(email),
        )

        user.set_password(password)
        user.is_admin = True
        user.save()

        return user


class CustomizedUser(AbstractBaseUser):
    username = models.CharField(max_length=20, verbose_name='username',
                                unique=True)
    email = models.EmailField(max_length=255, verbose_name='email address',
                              unique=True)
    vk_page = models.CharField(max_length=40, null=True, blank=True,
                               verbose_name='страница в вк')

    date_of_birth = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomizedUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        return self.is_admin
