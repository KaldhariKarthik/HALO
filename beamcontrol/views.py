from django.shortcuts import render
from .camera import detect_brightness

def index(request):
    brightness, text = detect_brightness()
    return render(request, 'index.html', {'text': text})
