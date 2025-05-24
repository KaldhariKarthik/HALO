from django.urls import path
from . import views  # or from halo import views, if you're in project-level urls.py

urlpatterns = [
    path('', views.index, name='index'),
    path('video_feed/', views.video_feed, name='video_feed'),
    path('detection_status/', views.detection_status, name='detection_status'),
    path('flashlight_data/', views.flashlight_data, name='flashlight_data'),  # ✅ THIS LINE IS MISSING
]

