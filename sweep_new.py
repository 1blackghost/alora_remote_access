import time
import cv2
from ultralytics import YOLO
import threading
import math
import bridge

# Initialize YOLO model
model = YOLO("red.pt")  
cap = cv2.VideoCapture(1)

# Constants
CONFIDENCE_THRESHOLD = 0.8
L1 = 10  
L2 = 10  

# Bridge setup
s = bridge.Element
s.start()
s.send("23", "140")

# Camera center threshold (tolerance)
CENTER_TOLERANCE = 20  # Pixels

def calculate_servo_angles(x, y):
    """Calculate the servo angles using inverse kinematics."""
    base_angle = math.degrees(math.atan2(y, x))
    base_angle_offset = base_angle - 90  

    D = math.sqrt(x**2 + y**2)
    D = min(max(D, abs(L1 - L2)), L1 + L2)  

    cos_theta2 = (D**2 - L1**2 - L2**2) / (2 * L1 * L2)
    elbow_angle = math.degrees(math.acos(cos_theta2))

    theta1 = math.degrees(math.atan2(y, x))
    cos_alpha = (L1**2 + D**2 - L2**2) / (2 * L1 * D)
    alpha = math.degrees(math.acos(cos_alpha))
    
    shoulder_angle = (theta1 - alpha)  
    elbow_angle = 180 - elbow_angle  

    shoulder_angle = 90 - shoulder_angle  
    elbow_angle = 180 - elbow_angle  

    base_angle = max(0, min(180, base_angle + 90))
    shoulder_angle = max(0, min(180, shoulder_angle))
    elbow_angle = max(0, min(180, elbow_angle))

    return base_angle - 40 + 20, 180 + 10 - shoulder_angle + 25, elbow_angle + 20

def start_sweep():
    """Continuously sweeps the camera left and right until the cube is detected."""
    angle = 90
    step = 5
    while True:
        angle += step
        time.sleep(0.2)
        s.send("14", str(angle))
        
        if angle > 180:
            step = -5
        if angle < 0:
            step = 5

def detect_and_center_cube():
    """Detects the red cube and centers it in the camera frame."""
    threading.Thread(target=start_sweep).start()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_height, frame_width = frame.shape[:2]
        center_x, center_y = frame_width // 2, frame_height // 2

        results = model(frame, conf=CONFIDENCE_THRESHOLD)
        detected = False

        for r in results:
            for box in r.boxes.xyxy:
                x1, y1, x2, y2 = map(int, box)  
                x_center = (x1 + x2) // 2
                y_center = (y1 + y2) // 2

                # Draw rectangle around the detected cube
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  

                # Check if the cube is centered
                if abs(x_center - center_x) < CENTER_TOLERANCE and abs(y_center - center_y) < CENTER_TOLERANCE:
                    detected = True
                    print(f"Centered Cube at X: {x_center}, Y: {y_center}")
                    cv2.putText(frame, "CENTERED!", (x_center - 50, y_center - 20), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

                # Display coordinates
                print(f"Detected at X: {x_center}, Y: {y_center}")
                break

        # Display the camera feed
        cv2.imshow("Red Cube Detection", frame)

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        # Stop sweeping if the cube is detected and centered
        if detected:
            print("Cube is centered. Stopping sweep.")
            break

    cap.release()
    cv2.destroyAllWindows()

# Start the detection and centering process
detect_and_center_cube()
