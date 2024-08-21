# import json

# print(json.dumps({0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 5: 'bus', 6: 'train', 7: 'truck', 8: 'boat', 9: 'traffic light', 10: 'fire hydrant', 11: 'stop sign', 12: 'parking meter', 13: 'bench', 14: 'bird', 15: 'cat', 16: 'dog', 17: 'horse', 18: 'sheep', 19: 'cow', 20: 'elephant', 21: 'bear', 22: 'zebra', 23: 'giraffe', 24: 'backpack', 25: 'umbrella', 26: 'handbag', 27: 'tie', 28: 'suitcase', 29: 'frisbee', 30: 'skis', 31: 'snowboard', 32: 'sports ball', 33: 'kite', 34: 'baseball bat', 35: 'baseball glove', 36: 'skateboard', 37: 'surfboard', 38: 'tennis racket', 39: 'bottle', 40: 'wine glass', 41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl', 46: 'banana', 47: 'apple', 48: 'sandwich', 49: 'orange', 50: 'broccoli', 51: 'carrot', 52: 'hot dog', 53: 'pizza', 54: 'donut', 55: 'cake', 56: 'chair', 57: 'couch', 58: 'potted plant', 59: 'bed', 60: 'dining table', 61: 'toilet', 62: 'tv', 63: 'laptop', 64: 'mouse', 65: 'remote', 66: 'keyboard', 67: 'cell phone', 68: 'microwave', 69: 'oven', 70: 'toaster', 71: 'sink', 72: 'refrigerator', 73: 'book', 74: 'clock', 75: 'vase', 76: 'scissors', 77: 'teddy bear', 78: 'hair drier', 79: 'toothbrush'}, indent=4))


import cv2
import numpy as np
import supervision as sv
from ultralytics import YOLO
import time

# import logging
# logging.basicConfig(level=logging.ERROR)
import requests


model = YOLO("yolov8n.pt")
tracker = sv.ByteTrack()
box_annotator = sv.BoxAnnotator()
label_annotator = sv.LabelAnnotator()
trace_annotator = sv.TraceAnnotator()


def callback(frame: np.ndarray, _: int) -> np.ndarray:
    results = model(frame)[0]
    detections = sv.Detections.from_ultralytics(results)
    detections = tracker.update_with_detections(detections)

    labels = [
        f"#{tracker_id} {results.names[class_id]}"
        for class_id, tracker_id in zip(detections.class_id, detections.tracker_id)
    ]

    annotated_frame = box_annotator.annotate(frame.copy(), detections=detections)
    annotated_frame = label_annotator.annotate(
        annotated_frame, detections=detections, labels=labels
    )
    return trace_annotator.annotate(annotated_frame, detections=detections)


def send_telegram_message(bot_token, chat_id, message):
    """
    Sends a message to a Telegram chat.

    Parameters:
    - bot_token (str): The token of the Telegram bot.
    - chat_id (str): The ID of the chat to send the message to.
    - message (str): The message to send.

    Returns:
    - response (dict): The response from the Telegram API.
    """
    send_message_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    response = requests.post(send_message_url, data=payload)
    return response.json()


bot_token = "7063368407:AAHFXUgXDZBw4LkC4q-jLkBNgwJxQ2qw4yw"
chat_id = "-1002043489442"
camera = cv2.VideoCapture(0)  # 0 is usually the default camera
# Initialize recording state and start time
is_recording = False
start_time = 0
record_duration = 20  # seconds

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*"MP4V")
print(camera.get(3), camera.get(4))
out = cv2.VideoWriter(
    "output.mp4", fourcc, 20.0, (int(camera.get(3)), int(camera.get(4)))
)


while True:
    ret, frame = camera.read()
    if not ret:
        print("Failed to grab frame")
        break

    processed_frame = callback(frame, 0)
    print(is_recording, "is recording")

    # Check if objects were detected
    if len(sv.Detections.from_ultralytics(model(frame)[0])) > 0:
        if not is_recording:
            is_recording = True
            start_time = time.time()
            # Send a message to the Telegram chat when an object is detected and recording starts
            message = "Object detected! Starting recording."
            send_telegram_message(bot_token, chat_id, message)
        elif time.time() - start_time < record_duration:
            is_recording = True
        else:
            is_recording = False
    elif is_recording and time.time() - start_time < record_duration:
        is_recording = True
    else:
        is_recording = False

    # Record if in recording state
    if is_recording:
        out.write(processed_frame)

    # Display the processed frame
    cv2.imshow("Processed Frame", processed_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):  # Press 'q' to quit
        break

camera.release()
out.release()
cv2.destroyAllWindows()
