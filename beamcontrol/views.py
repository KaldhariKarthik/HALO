from django.http import StreamingHttpResponse
from django.shortcuts import render
from .utils import gen_frames
from django.http import JsonResponse
from .utils import last_detection


def index(request):
    # Change this line depending on your folder structure and settings.py
    return render(request, 'index.html')  # or 'index.html' if you move template


def video_feed(request):
    return StreamingHttpResponse(gen_frames(), content_type='multipart/x-mixed-replace; boundary=frame')


def detection_status(request):
    if last_detection['detected']:
        coords_str = ','.join(map(str, last_detection['coords']))
    else:
        coords_str = '- - - -'
    return JsonResponse({
        'detected': last_detection['detected'],
        'coords': coords_str
    })