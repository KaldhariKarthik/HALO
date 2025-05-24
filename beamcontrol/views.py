from django.http import StreamingHttpResponse, JsonResponse
from django.shortcuts import render
from .utils import gen_frames, get_flashlight_coordinates, last_detection

def index(request):
    return render(request, 'index.html')

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

def flashlight_data(request):
    coords = get_flashlight_coordinates()
    return JsonResponse({"coordinates": coords})
