from django.db import models
from django.contrib.auth.models import User

class UserCommunity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    community_picture = models.ImageField(upload_to='community_picture/', null=True, blank=True)
    description = models.TextField()
    create_time = models.DateTimeField(auto_now=True)

class CommunityRole(models.Model):
    community = models.ForeignKey(UserCommunity, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    adding_post_permission = models.BooleanField(default=False)
    comment_post_permission = models.BooleanField(default=False)
    adding_image_permission = models.BooleanField(default=False)
    adding_video_permission = models.BooleanField(default=False)
    adding_vote_permission = models.BooleanField(default=False)
    adding_answer_vote_permission = models.BooleanField(default=False)
    user_ban_permission = models.BooleanField(default=False)
    user_mute_permission = models.BooleanField(default=False)
    delete_user_post_permission = models.BooleanField(default=False)
    admin_permission = models.BooleanField(default=False)

    def has_permission(self, permission_name):
        return getattr(self, permission_name, False)


class CommunityMember(models.Model):
    community = models.ForeignKey(UserCommunity, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(CommunityRole, on_delete=models.CASCADE, null=True, blank=True)
    joining_time = models.DateTimeField(auto_now=True)


class CommunityPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(UserCommunity, on_delete=models.CASCADE)
    text = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='image/', null=True, blank=True)
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    role = models.ForeignKey(CommunityRole, on_delete=models.CASCADE, null=True, blank=True)


class CommunityPoll(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(UserCommunity, on_delete=models.CASCADE)
    question = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)


class PollAnswer(models.Model):
    poll = models.ForeignKey(CommunityPoll, on_delete=models.CASCADE)
    text = models.TextField()


class UserPollAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pollanswer = models.ForeignKey(PollAnswer, on_delete=models.CASCADE)
    add_time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'pollanswer')


class CommunityChat(models.Model):
    community = models.ForeignKey(UserCommunity, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()


class ChatMessage(models.Model):
    chat = models.ForeignKey(CommunityChat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    add_time = models.DateTimeField(auto_now=True)
