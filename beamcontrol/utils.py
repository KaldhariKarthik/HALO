import cv2
import numpy as np
from .inference import detect_objects_from_frame  # Your detector

# Global variables
last_detection = {
    'detected': False,
    'coords': None,
}

last_detections = []  # List of all flashlight detections


def gen_frames():
    global last_detection, last_detections

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not open webcam.")

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)  # Mirror horizontally

        detections = detect_objects_from_frame(frame)
        flashlight_detected = False
        flashlight_coords = []

        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            cls_id = det['class_id']
            conf = det['confidence']
            label = f"Class {cls_id} ({conf:.2f})"

            if cls_id == 0:  # Flashlight class
                flashlight_detected = True
                flashlight_coords.append((x1, y1, x2, y2))
                color = (0, 0, 255)  # Red for flashlight
                cv2.putText(frame, "Flashlight", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            else:
                color = (0, 255, 0)  # Green for others

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

        # Update global status
        last_detection['detected'] = flashlight_detected
        last_detection['coords'] = flashlight_coords[0] if flashlight_coords else None
        last_detections = flashlight_coords

        if flashlight_detected:
            cv2.putText(frame, "Flashlight Detected!", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()


def get_flashlight_coordinates():
    # Converts (x1, y1, x2, y2) to dictionary list
    return [{"x1": x1, "y1": y1, "x2": x2, "y2": y2} for (x1, y1, x2, y2) in last_detections]
