from django.http import StreamingHttpResponse
from django.shortcuts import render
from .utils import gen_frames

def index(request):
    # Change this line depending on your folder structure and settings.py
    return render(request, 'index.html')  # or 'index.html' if you move template


def video_feed(request):
    return StreamingHttpResponse(gen_frames(), content_type='multipart/x-mixed-replace; boundary=frame')
