import cv2
import numpy as np
from .inference import detect_objects_from_frame  # Your detector

# Global variable to hold detection info
last_detection = {
    'detected': False,
    'coords': None,
}

def gen_frames():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not open webcam.")
    
    while True:
        success, frame = cap.read()
        if not success:
            break
        
        # Mirror the frame horizontally (flip around y-axis)
        frame = cv2.flip(frame, 1)
        
        # --- YOLOv5 AI Detection start ---
        detections = detect_objects_from_frame(frame)
        flashlight_detected = False
        coords = None

        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            cls_id = det['class_id']
            conf = det['confidence']
            label = f"Class {cls_id} ({conf:.2f})"

            # Check if this is flashlight class (replace 0 with your actual class id)
            if cls_id == 0:
                flashlight_detected = True
                coords = (x1, y1, x2, y2)

            # Draw bounding box: RED for flashlight, GREEN otherwise
            color = (0, 0, 255) if cls_id == 0 else (0, 255, 0)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        # If flashlight detected, put text in red on top-left corner
        if flashlight_detected:
            cv2.putText(frame, "Flashlight Detected!", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Update global detection info (used by your Django JSON status view)
        last_detection['detected'] = flashlight_detected
        last_detection['coords'] = coords

        # Encode the processed frame as JPEG for streaming
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    
    cap.release()
