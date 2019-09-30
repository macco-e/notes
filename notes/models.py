from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django_mysql.models import ListCharField


# class AccountManager(UserManager):
#     def _create_user(self, username, password, **extra_fields):
#         user = self.model(**extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_user(self, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', False)
#         extra_fields.setdefault('is_superuser', False)
#         return self._create_user(password, **extra_fields)
#
#     def create_superuser(self, username, password, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         return self._create_user(password, **extra_fields)


class Account(AbstractUser):
    noted_num = models.IntegerField(default=0)
    noted_tables = ListCharField(
        base_field=models.CharField(max_length=16, null=True, blank=True),
        size=52,
        max_length=(17 * 53),
        blank=True
    )
    icon = models.ImageField(upload_to='', blank=True, default='')


class Follow(models.Model):
    follower_id = models.ForeignKey(Account, on_delete=models.CASCADE,
                                    related_name='follower_id')
    follow_id = models.ForeignKey(Account, on_delete=models.CASCADE,
                                  related_name='follow_id')


class NotesBetween20190930and20191006(models.Model):
    noted_user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    text = models.TextField()
    commented_users_id = ListCharField(
        base_field=models.IntegerField(),
        max_length=100,
        blank=True
    )
    created_at = models.DateTimeField()
    images = models.ImageField(upload_to='', blank=True, default='')
