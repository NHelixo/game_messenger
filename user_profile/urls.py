from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'user_profile'

urlpatterns = [
    path('profile/<int:pk>/', views.Profile.as_view(), name='profile'),
    path('edit_profile/<int:pk>/', views.ProfileEdit.as_view(), name='edit_profile'),
    path('friends/<int:pk>/', views.FriendList.as_view(), name='friends'),
    path('comfirm_friend/<int:pk>/', views.AcceptFriend.as_view(), name='comfirm_friend'),
    path('reject_friend/<int:pk>/', views.RejectFriend.as_view(), name='reject_friend'),
    path('communities/', views.Communities.as_view(), name='communities'),
    path('chat/<int:pk>/', views.ChatDetailView.as_view(), name='chat_detail'),
    path('chat/create/', views.ChatCreateView.as_view(), name='chat_create'),
    path('chat/message/create/', views.ChatMessageCreateView.as_view(), name='chat_message_create'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
