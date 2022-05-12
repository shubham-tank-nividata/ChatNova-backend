from django.db import models
from django.utils import timezone
from users.models import Account

class Post(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    content = models.CharField(max_length=280)
    image = models.ImageField(null=True, blank=True,upload_to='post_pics')
    created_at = models.DateTimeField(default=timezone.now)

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=280)
    created_at = models.DateTimeField(default=timezone.now)