import cv2
import numpy as np
import mss
from ultralytics import YOLO
import pyttsx3

from utils.screen_capture import capture_screen

engine = pyttsx3.init()
engine.setProperty('rate', 150)

model = YOLO("best.pt")

CONFIDENCE_THRESHOLD = 0.5
FRAMES_REQUIRED = 5

class_frame_counts = {}
spoken_classes = set()

with mss.mss() as sct:
    while True:
        img = capture_screen()
        frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        results = model(frame)
        annotated_frame = results[0].plot()

        classes = results[0].names
        detected_ids = results[0].boxes.cls.cpu().numpy().astype(int)
        confidences = results[0].boxes.conf.cpu().numpy()

        current_classes = set()
        for cls_id, conf in zip(detected_ids, confidences):
            if conf >= CONFIDENCE_THRESHOLD:
                current_classes.add(classes[cls_id])

        # Update frame counts
        for cls in current_classes:
            class_frame_counts[cls] = class_frame_counts.get(cls, 0) + 1

        # Remove or reset classes not detected this frame
        to_delete = []
        for cls in class_frame_counts:
            if cls not in current_classes:
                class_frame_counts[cls] = 0
                to_delete.append(cls)
        # Clean up zero-count classes to avoid clutter
        for cls in to_delete:
            del class_frame_counts[cls]

        # Debug: print frame counts
        print("Frame counts:", class_frame_counts)

        # Speak classes that have reached threshold and not spoken yet
        for cls, count in class_frame_counts.items():
            if count >= FRAMES_REQUIRED and cls not in spoken_classes:
                print(f"Saying: {cls}")
                engine.say(cls)
                engine.runAndWait()
                spoken_classes.add(cls)

        cv2.imshow("YOLOv8 Inference", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cv2.destroyAllWindows()
