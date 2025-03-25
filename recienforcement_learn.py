import time
import cv2
from ultralytics import YOLO
import threading
import math
import bridge

# Load YOLO model
model = YOLO("red.pt")  

# Open camera
cap = cv2.VideoCapture(1)

# Confidence threshold for YOLO
CONFIDENCE_THRESHOLD = 0.8

# Robot arm lengths
L1 = 10  
L2 = 10  

# Start bridge connection
s = bridge.Element
s.start()

# Clamp control limits
CLAMP_CLOSE = 80  
CLAMP_OPEN = 150  

# Initial clamp position
s.send("23", str(CLAMP_OPEN))

def calculate_servo_angles(x, y):
    """Calculate servo angles based on x, y coordinates."""
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

def clamp_control(position):
    """Clamp control with safety limits."""
    position = max(CLAMP_CLOSE, min(CLAMP_OPEN, position))
    s.send("24", str(position))

def mover(x, y, z):
    """Move the robot arm to x, y, z coordinates."""
    global s

    # Close clamp
    clamp_control(CLAMP_CLOSE)
    time.sleep(0.5)

    # Move servos
    s.send("14", str(x))
    time.sleep(3)
    s.send("15", str(y))
    time.sleep(2)
    s.send("18", str(z))
    time.sleep(2)

    # Open clamp
    clamp_control(CLAMP_OPEN)
    time.sleep(2)

    # Reset position
    s.send("14", "90")
    time.sleep(2)
    s.send("15", "90")
    time.sleep(2)
    s.send("18", "90")
    time.sleep(2)
    clamp_control(CLAMP_OPEN)
    time.sleep(2)

    # Move to the blue basket
    s.send("14", "180")
    time.sleep(4)
    s.send("15", "150")
    time.sleep(2)
    s.send("18", "30")
    time.sleep(2)

    # Drop the cube
    clamp_control(CLAMP_OPEN)
    time.sleep(3)

    # Return to home position
    time.sleep(2)
    s.send("15", "90")
    time.sleep(2)
    s.send("18", "90")
    time.sleep(2)
    clamp_control(CLAMP_OPEN)
    time.sleep(2)
    s.send("14", "90")

def move_the_arm(cx, cy):
    """Calculate servo angles and move the arm."""
    x, y, z = calculate_servo_angles(cx, cy)
    x = int(x - 25)
    y = int(y + 28)
    z = int(z)

    threading.Thread(target=mover, args=(x, y, z)).start()
    print(f"Moving arm to pos: X={x}, Y={y}, Z={z}")

def detect_red_cube():
    """Detect red cubes and move the arm."""
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Suppress YOLOv8 output
        with open('yolo_logs.txt', 'w') as f:
            results = model(frame, conf=CONFIDENCE_THRESHOLD, verbose=False)

        detected = False  
        for r in results:
            for box in r.boxes.xyxy:
                x1, y1, x2, y2 = map(int, box)  
                x_center = (x1 + x2) // 2
                y_center = (y1 + y2) // 2
                z = 100  

                # Draw rectangle around the detected cube
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # Display coordinates and status
                cv2.putText(frame, f"X: {x_center}, Y: {y_center}, Z: {z}",
                            (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                cv2.putText(frame, "Status: DETECTED", 
                            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                detected = True
                print(f"Detected at X: {x_center}, Y: {y_center}, Z: {z}")
                break

            if detected:
                break

        if detected:
            threading.Thread(target=move_the_arm, args=(x_center, y_center)).start()
            break

        # Display the frame with detection info
        cv2.imshow("YOLOv8 Cube Detection", frame)

        # Quit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

# Start the detection process
detect_red_cube()
