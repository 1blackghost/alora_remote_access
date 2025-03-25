import time
import cv2
from ultralytics import YOLO
import threading
import math
import bridge
import speak

model = YOLO("red.pt")  

cap = cv2.VideoCapture(1)

CONFIDENCE_THRESHOLD = 0.8

L1 = 10 
L2 = 10  

def descrp():
    descption='''
    Hello everyone! 
    I am Alora, the robotic arm designed to aid the blind, assist with household tasks, 
    and contribute to remote manufacturing. 
    I can pick up objects, manipulate tools, and perform various tasks with precision.

    Right now, I am doing a little "hi" emote. Hello everybody! 

    Even though I am only ten days old, still just a child in the robotic world, 
    I am already exploring and learning new things every day. Heheh!
    Who knows what I will be able to do next?


    '''
    speak.speak(descption)

s=bridge.Element
s.start()
s.send("23","140")
time.sleep(0.5)
threading.Thread(target=descrp,args=()).start()
while True:
    s.send("15","110")
    time.sleep(0.2)
    s.send("18","115")
    time.sleep(2.5)
    s.send("15","70")
    time.sleep(0.2)
    s.send("18","65")
    time.sleep(2.5)


