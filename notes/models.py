from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django_mysql.models import ListCharField
from django.utils.html import mark_safe
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill
from markdown import markdown


class Account(AbstractUser):
    noted_num = models.IntegerField(default=0)
    noted_tables = ListCharField(
        base_field=models.CharField(max_length=16, null=True, blank=True),
        size=52,
        max_length=(17 * 53),
        blank=True
    )
    icon = models.ImageField(upload_to='icons', blank=True, default='icons/iconfinder_profle_1055000.png')

    icon_small = ImageSpecField(
        source='icon',
        processors=[ResizeToFill(32, 32)],
        format='JPEG',
    )

    icon_middle = ImageSpecField(
        source='icon',
        processors=[ResizeToFill(70, 70)],
        format='JPEG'
    )

    icon_big = ImageSpecField(
        source='icon',
        processors=[ResizeToFill(150, 150)],
        format='JPEG'
    )


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

    def get_text_as_markdown(self):
        return mark_safe(markdown(self.text, safe_mode='escape'))
