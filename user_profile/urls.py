from django.urls import path
from . import views
from .views import Profile, ProfileEdit
from django.conf import settings
from django.conf.urls.static import static

app_name = 'user_profile'

urlpatterns = [
    path('profile/<int:pk>/', views.Profile.as_view(), name='profile'),
    path('edit_profile/<int:pk>/', views.ProfileEdit.as_view(), name='edit_profile'),
    path('friends/<int:pk>/', views.FriendList.as_view(), name='friends'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
