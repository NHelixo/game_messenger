from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'community'

urlpatterns = [
    path('<int:id>/', views.Community.as_view(), name='community'),
    path('add_role/<int:id>/', views.AddRole.as_view(), name='add_role'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
