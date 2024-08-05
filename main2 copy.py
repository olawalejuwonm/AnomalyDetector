import cv2
import numpy as np
import supervision as sv
from ultralytics import YOLO
import time
# import logging
# logging.basicConfig(level=logging.ERROR)
import requests
import os
import datetime



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
        for class_id, tracker_id
        in zip(detections.class_id, detections.tracker_id)
    ]

    annotated_frame = box_annotator.annotate(
        frame.copy(), detections=detections)
    annotated_frame = label_annotator.annotate(
        annotated_frame, detections=detections, labels=labels)
    return trace_annotator.annotate(
        annotated_frame, detections=detections)

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
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    response = requests.post(send_message_url, data=payload)
    return response.json()
bot_token = "7063368407:AAHFXUgXDZBw4LkC4q-jLkBNgwJxQ2qw4yw"
chat_id = "-1002043489442"
camera = cv2.VideoCapture(0)  # 0 is usually the default camera
# Initialize recording state and start time
is_recording = False
start_time = 0
record_duration = 20  # seconds


# Step 1: Define the directory path
video_directory = "static/recorded_videos"

# Step 2: Check if the directory exists, if not, create it
if not os.path.exists(video_directory):
    os.makedirs(video_directory)

# Define the codec and create VideoWriter object
# fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Change 'MP4V' to 'mp4v'
def start_new_recording():
    output_file = f'output_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.webm'
    return cv2.VideoWriter(os.path.join(video_directory, output_file), fourcc, 20.0, (int(camera.get(3)), int(camera.get(4))))

fourcc = cv2.VideoWriter_fourcc(*'VP90')
out = None

while True:
    ret, frame = camera.read()
    if not ret:
        print("Failed to grab frame")
        break

    processed_frame = callback(frame, 0)
    detected_objects = sv.Detections.from_ultralytics(model(frame)[0])

    if len(detected_objects) > 0:
        if not is_recording:
            is_recording = True
            out = start_new_recording()  # Start a new recording with a new timestamp
            class_ids = detected_objects.class_id
            object_names = [model.names[class_id] for class_id in class_ids]
            message = f"Object detected! Starting recording. Detected objects: {', '.join(object_names)}."
            send_telegram_message(bot_token, chat_id, message)
    else:
        if is_recording:
            is_recording = False
            out.release()  # Stop the current recording

    if is_recording:
        out.write(processed_frame)

    cv2.imshow('Processed Frame', processed_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
if is_recording:
    out.release()
cv2.destroyAllWindows()