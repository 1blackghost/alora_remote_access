import torch
import whisper
import sounddevice as sd
import numpy as np
import wave
import subprocess
import re
import threading
import speak
import time
import bridge

def descrp(description):
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

def move_emote():
    s = bridge.Element
    s.start()
    s.send("15", "110")  
    time.sleep(0.2)
    s.send("18", "115")  
    time.sleep(2.5)

def cross_emote():
    s = bridge.Element
    s.start()
    s.send("15", "70")   
    time.sleep(0.2)
    s.send("18", "65")   
    time.sleep(2.5)

def engage_emote():
    s = bridge.Element
    s.start()
    s.send("14", "160")  
    s.send("15", "160")
    time.sleep(1)

def process_text(sentence):
    keywords = {
        "pick": ["pick", "grab", "take"],
        "hello": ["hello", "hi", "hey"],
        "move": ["walk", "move", "go"],
        "wave": ["wave", "greet"],
        "cross": ["cross arms", "fold arms"],
        "engage": ["listen", "talk", "speak"]
    }
    
    words = sentence.lower()
    
    for key, values in keywords.items():
        for value in values:
            if re.search(rf'\b{value}\b', words):
                return key
    
    return None

def record_audio(filename="audio.wav", duration=5, samplerate=16000):
    while True:
        print("Recording...")
        audio_data = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype=np.int16)
        sd.wait()
        
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(samplerate)
            wf.writeframes(audio_data.tobytes())
        
        yield filename 

def transcribe_audio(filename="audio.wav", model_size="base"):
    model = whisper.load_model(model_size)
    result = model.transcribe(filename)
    return result["text"]

def engage_conversation():
    for audio_file in record_audio():
        print("Processing...")
        text = transcribe_audio(audio_file)
        print("Transcription:", text)
        result = process_text(text)
        print(result)
        
        if result == "pick" or result == "take":
            subprocess.run(["python", "red_blue.py"])
        elif result == "hello" or result == "hi" or result == "hey":
            des = "Hello there, what's going on?"
            threading.Thread(target=descrp, args=(des,)).start()
            threading.Thread(target=wave_emote, args=()).start()
        elif result == "move":
            threading.Thread(target=move_emote, args=()).start()
        elif result == "wave":
            threading.Thread(target=wave_emote, args=()).start()
        elif result == "engage":
            threading.Thread(target=engage_emote, args=()).start()
        else:
            threading.Thread(target=cross_emote, args=()).start()


def engage_conversation():
        text=input("Enter the prompt: ")
        result = process_text(text)
        
        if result == "pick" or result == "take":
            speak.speak("Ookey searching and picking the red cube...")
            subprocess.run(["python", "red_blue.py"])
        elif result == "hello" or result == "hi" or result == "hey":
            des = "Hello there, what's going on?"
            threading.Thread(target=descrp, args=(des,)).start()
            threading.Thread(target=wave_emote, args=()).start()
        elif result == "move":
            threading.Thread(target=move_emote, args=()).start()
        elif result == "wave":
            threading.Thread(target=wave_emote, args=()).start()
        elif result == "engage":
            threading.Thread(target=engage_emote, args=()).start()
        else:
            threading.Thread(target=cross_emote, args=()).start()

if __name__ == "__main__":
    engage_conversation()
