from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django_mysql.models import ListCharField


class Account(AbstractUser):
    noted_num = models.IntegerField(default=0)
    noted_tables = ListCharField(
        base_field=models.CharField(max_length=16, null=True, blank=True),
        size=52,
        max_length=(17 * 53),
        blank=True
    )
    icon = models.ImageField(upload_to='icons', blank=True, default='')


class Follow(models.Model):
    follower_id = models.ForeignKey(Account, on_delete=models.CASCADE,
                                    related_name='follower_id')
    follow_id = models.ForeignKey(Account, on_delete=models.CASCADE,
                                  related_name='follow_id')


class NotesBetween20190930and20191006(models.Model):
    noted_user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    text = models.TextField(blank=True, default='')
    commented_users_id = ListCharField(
        base_field=models.IntegerField(),
        max_length=100,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    images = models.ImageField(upload_to='', blank=True, default='')
