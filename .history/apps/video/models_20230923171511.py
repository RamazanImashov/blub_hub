from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
User = get_user_model()

class Topics(models.Model):
    title = models.CharField(max_length=50, unique=True, verbose_name='Topics_name')
    slug = models.SlugField(max_length=30, primary_key=True, blank=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save()


class Video(models.Model):
    topics = models.ForeignKey(Topics, on_delete=models.CASCADE, related_name='topics', verbose_name='Topics')
    videos = models.FileField(blank=False, upload_to='videos/')
    video_preview = models.ImageField(blank=False, upload_to='video_preview/')
    title = models.CharField(max_length=130, verbose_name='Название', unique=True)
    slug = models.SlugField(primary_key=True, max_length=30, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save()

    def get_description(self):
        return self.description

class Subscription(models.Model):
    subscriber = models.ForeignKey(User, related_name='subscriptions', on_delete=models.CASCADE)
    target_user = models.ForeignKey(User, related_name='subscribers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
