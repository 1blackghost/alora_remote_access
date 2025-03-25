import cv2
import torch
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import bridge
import speak
import time

def capture_image():
    time.sleep(1)
    cap = cv2.VideoCapture(1)  
    if not cap.isOpened():
        print("Error: Could not access webcam")
        return None

    ret, frame = cap.read()
    cap.release()

    if ret:
        image_path = "img.jpg"
        cv2.imwrite(image_path, frame)
        print(f"Image saved as {image_path}")
        speak.speak("Creating description from the snippet..")
        return image_path
    else:
        print("Failed to capture image")
        return None


def generate_caption(image_path):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)

    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt").to(device)

    with torch.no_grad():
        caption_ids = model.generate(**inputs)

    caption = processor.decode(caption_ids[0], skip_special_tokens=True)
    return caption


def main():
    image_path = capture_image()

    if image_path:
        caption = generate_caption(image_path)
        print("\n📝 Generated Caption:", caption)
        time.sleep(2)
        speak.speak("Results are: "+str(caption))
    else:
        print("No image captured. Exiting.")


if __name__ == "__main__":



    s=bridge.Element
    s.start()
    s.send("23","140")
    speak.speak("connection sucessful!")
    time.sleep(3)
    speak.speak("Scanning the surrounding for making descriptions ")
    s.send("14","0")
    time.sleep(2)
    main()
    s.send("14","60")
    time.sleep(2)

    main()
    s.send("14","120")
    time.sleep(2)

    main()

    s.send("14","180")
    time.sleep(2)

    main()
    time.sleep(2)
    speak.speak("Exiting program")
