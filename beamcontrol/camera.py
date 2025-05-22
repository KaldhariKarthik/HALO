import cv2
import numpy as np

def detect_brightness():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        return 0, "Camera Error"

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    avg_brightness = np.mean(gray)

    if avg_brightness > 100:
        return avg_brightness, "High Beam"
    else:
        return avg_brightness, "Low Beam"
