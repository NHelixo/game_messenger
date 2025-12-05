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


class UserPicture(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='profile_pictures/default.jpg', null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
