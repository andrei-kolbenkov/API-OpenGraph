from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)


class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collections')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} | {self.user}"

    class Meta:
        verbose_name = 'Коллекция'
        verbose_name_plural = 'Коллекции'

class Link(models.Model):
    TYPE_CHOICES = [
        ('website', 'Website'),
        ('book', 'Book'),
        ('article', 'Article'),
        ('music', 'Music'),
        ('video', 'Video'),
    ]
    url = models.URLField()
    link_type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='website')
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='links')
    collections = models.ManyToManyField(Collection, related_name='links', blank=True)
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} | {self.link_type} | {self.user} | {self.collections}"

    class Meta:
        unique_together = ('user', 'url')
        verbose_name = 'Ссылка'
        verbose_name_plural = 'Ссылки'
