from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import mark_safe
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from markdown import markdown


class Account(AbstractUser):
    icon = models.ImageField(upload_to='icons', blank=True, default='icons/default.png')

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

    def __str__(self):
        return self.username


class Follow(models.Model):
    follow = models.ForeignKey(Account, on_delete=models.CASCADE,
                                  related_name='follow_id')
    follower = models.ForeignKey(Account, on_delete=models.CASCADE,
                                    related_name='follower_id')

    def __str__(self):
        return f'{self.follow.username}-{self.follower.username}'


class Notes(models.Model):
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    text = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    images = models.ImageField(upload_to='', blank=True, default='')

    class Meta:
        ordering = ['-created_at']

    def get_markdown(self):
        return markdown(self.text)

    def get_text_as_markdown(self):
        # fenced_code - ```code```
        # nl2br - new line to break
        # https://python-markdown.github.io/reference/
        return mark_safe(markdown(self.text, extensions=['fenced_code', 'attr_list', 'nl2br'], safe_mode='escape'))

    def get_format_created_at(self):
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return f'{self.author}:{self.text[:5]}'
