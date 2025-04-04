import cv2
import mediapipe as mp
import time
import subprocess
import speak
import bridge
import threading


def descrpi(description):
    speak.speak(description)

def wave_emote():
    s = bridge.Element
    s.start() 
    s.send("23","140")
    time.sleep(0.5)
    s.send("14","90")
    time.sleep(0.5)
    while True:
        s.send("15","110")
        time.sleep(0.2)
        s.send("18","115")
        time.sleep(2.5)
        s.send("15","70")
        time.sleep(0.2)
        s.send("18","65")
        time.sleep(2.5)


def recognize_hi_gesture(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[4]
    index_tip = hand_landmarks.landmark[8]
    middle_tip = hand_landmarks.landmark[12]
    ring_tip = hand_landmarks.landmark[16]
    pinky_tip = hand_landmarks.landmark[20]
    index_mcp = hand_landmarks.landmark[5]

    if (index_tip.x < index_mcp.x and
        middle_tip.y > index_mcp.y and
        ring_tip.y > index_mcp.y and
        pinky_tip.y > index_mcp.y and
        thumb_tip.y < index_tip.y):
        return "hi"
    return None

def on_hi_detected():
    descrp='''
    Hi thats a wave!!!!!hello there!
    '''
    threading.Thread(target=descrpi,args=(descrp,)).start()
    wave_emote()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(1)
last_gesture = None
last_time = time.time()

def print_gesture(gesture):
    global last_gesture, last_time
    if gesture and (gesture != last_gesture or time.time() - last_time > 2):
        print(f"Gesture Detected: {gesture}")
        last_gesture = gesture
        last_time = time.time()

        if gesture == "hi":
            on_hi_detected()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            gesture = recognize_hi_gesture(hand_landmarks)
            print_gesture(gesture)
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Hi Gesture Recognition", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
