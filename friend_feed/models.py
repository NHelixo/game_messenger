from django.db import models
from django.contrib.auth.models import User


class FriendPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    create_time = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='image/', null=True, blank=True)
    video = models.FileField(upload_to='videos/', null=True, blank=True)


class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(FriendPost, on_delete=models.CASCADE)


class PostComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(FriendPost, on_delete=models.CASCADE)
    text = models.TextField()
    owner_like = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now=True)
