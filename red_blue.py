import time
import cv2
from ultralytics import YOLO
import threading

# Load the YOLO model
model = YOLO("red.pt")  

# Open the webcam
cap = cv2.VideoCapture(1)

CONFIDENCE_THRESHOLD = 0.7  

def scanner_base():
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, conf=CONFIDENCE_THRESHOLD)

        detected = False  
        for r in results:
            for box in r.boxes.xyxy:
                x1, y1, x2, y2 = map(int, box)  
                x_center = (x1 + x2) // 2
                y_center = (y1 + y2) // 2
                z = 100  # Placeholder for depth value

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  
                detected = True
                print(f"Detected at X: {x_center}, Y: {y_center}, Z: {z}")

        cv2.imshow("YOLOv8 Live Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

# Start the detection thread
threading.Thread(target=scanner_base).start()
