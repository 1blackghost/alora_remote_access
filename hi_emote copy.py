import time
import cv2
from ultralytics import YOLO
import threading
import math
import bridge
import speak


def descrp(descption):
    speak.speak(descption)

degree=0

def invoke():
    global s,degree
    while True:
        if degree<=0:
            degree=0
            step=5
        elif degree>=180:
            degree=180
            step=-5
        degree+=step
        print(degree)
        time.sleep(1)       
        s.send("14",str(degree))
        time.sleep(2.5)

def emote():
    global s
    global degree
    threading.Thread(target=invoke,args=()).start()
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


if __name__=="__main__":
    s=bridge.Element
    s.start()
    descption='''
    Hello everyone! 
    I am Alora, the robotic arm designed to aid the blind, assist with household tasks, 
    and contribute to remote manufacturing. 
    I can pick up objects, manipulate tools, and perform various tasks with precision.

    Right now, I am doing a little "hi" emote. Hello everybody! 

    Even though I am only ten days old, still just a child in the robotic world, 
    I am already exploring and learning new things every day!
    Who knows what I will be able to do next?


    '''
    threading.Thread(target=descrp,args=(descption,)).start()
    emote()
