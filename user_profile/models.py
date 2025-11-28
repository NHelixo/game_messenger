from django.db import models
from django.contrib.auth.models import User

class UserFriend(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Очікує підтвердження'),
        ('accepted', 'Дружба підтверджена'),
        ('blocked', 'Заблокований'),
    )

    user = models.ForeignKey(User, related_name='user',on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='friend',on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending')


class ChatMessage(models.Model):
    user = models.ForeignKey(User, related_name='r_user', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='r_friend', on_delete=models.CASCADE)
    text = models.TextField()
    receiver_like = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)
    edited = models.BooleanField(default=False)
