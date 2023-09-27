from django.db import models
from apps.video.models import Video
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Comment(models.Model):
    body = models.TextField(verbose_name='Description')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    files = models.FileField(upload_to='comment_files/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author}, {self.body}'


class Rating(models.Model):
    rating = models.PositiveSmallIntegerField()
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='ratings')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')

    def __str__(self):
        return f'{self.author} {self.rating}'


class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return f'{self.author}{self.video}'


class Dislike(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dislikes')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='dislikes')

    def __str__(self):
        return f'{self.author}{self.video}'


class WatchLater(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watch_later')
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-pk',)
        constraints = [
            models.UniqueConstraint(fields=['author', 'video'], name='unique_author_video'),
        ]
        indexes = [
            models.Index(fields=['author', 'video'], name='index_author_video'),
        ]
    class Subscription(models.Model):
        subscriber = models.ForeignKey(User, related_name='subscriptions', on_delete=models.CASCADE)
        target_user = models.ForeignKey(User, related_name='subscribers', on_delete=models.CASCADE)
        created_at = models.DateTimeField(auto_now_add=True)
