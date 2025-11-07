from django.contrib import admin

from .models import CommunityRole, UserCommunity, CommunityMember, CommunityPost, CommunityPoll, PollAnswer, UserPollAnswer

admin.site.register([CommunityRole, UserCommunity, CommunityMember, CommunityPost, CommunityPoll, PollAnswer, UserPollAnswer])
