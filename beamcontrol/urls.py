from django.urls import path
from .views import index, video_feed, detection_status

urlpatterns = [
    path('', index, name='index'),
    path('video_feed/', video_feed, name='video_feed'),
    path('detection_status/', detection_status, name='detection_status'),
]
