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

    @classmethod
    def get_friendship(cls, user1, user2):
        return cls.objects.filter(
            (models.Q(user=user1) & models.Q(friend=user2)) |
            (models.Q(user=user2) & models.Q(friend=user1))
        ).first()


class Chat(models.Model):
    user = models.ForeignKey(User, related_name='c_user', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='c_receiver', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.receiver.username if self.user == self.receiver else f"{self.user.username} & {self.receiver.username}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('user', 'receiver')

class ChatMessage(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='r_user', on_delete=models.CASCADE)
    text = models.TextField()
    receiver_like = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)
    edited = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.user.username} to {self.chat.name}"


class UserPicture(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='profile_pictures/default.jpg', null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
