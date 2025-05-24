import torch
import cv2
import numpy as np

# Load YOLOv5 model (make sure yolov5 repo is in your path)
model = torch.hub.load('ultralytics/yolov5', 'custom', path='C:/Users/karth/Desktop/UPSKILL/HALO/PHASE1/runs/train/weights/best.pt', force_reload=True)

def detect_objects_from_frame(frame):
    results = model(frame)

    detections = []
    for *xyxy, conf, cls in results.xyxy[0]:
        if conf >= 0.65:  
            x1, y1, x2, y2 = map(int, xyxy)
            detections.append({
                "class_id": int(cls),
                "confidence": float(conf),
                "bbox": (x1, y1, x2, y2)
            })
    return detections
