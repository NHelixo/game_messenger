from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'friend_feed'

urlpatterns = [
    path('', views.PostFeed.as_view(), name='post_feed'),
    path('toggle_like/<int:post_id>/', views.ToggleLikeView.as_view(), name='toggle_like'),
    path('add_comment/<int:post_id>/', views.AddComment.as_view(), name='add_comment'),
    path('search_friend/', views.SearchFriend.as_view(), name='search_friend'),
    path('search_community/', views.SearchCommunity.as_view(), name='search_community'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
