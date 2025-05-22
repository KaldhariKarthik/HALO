import cv2
import numpy as np

def gen_frames():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not open webcam.")
    
    while True:
        success, frame = cap.read()
        if not success:
            break
        
        frame = cv2.flip(frame, 1)  # Mirror
        
        # --- Flashlight detection start ---
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Threshold to get very bright spots
        _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
        
        # Find contours of bright spots
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        flashlight_detected = False
        
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 100:  # tweak this threshold for size of bright spot
                # Draw bounding box around detected flashlight area
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
                flashlight_detected = True
        
        # Put detection text on frame
        if flashlight_detected:
            cv2.putText(frame, "Flashlight Detected!", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        # --- Flashlight detection end ---
        
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    cap.release()
