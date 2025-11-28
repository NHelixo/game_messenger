from django.urls import path
from . import views
from .views import Profile

app_name = 'user_profile'

urlpatterns = [
    path('profile/<int:pk>/', views.Profile.as_view(), name='profile'),
]