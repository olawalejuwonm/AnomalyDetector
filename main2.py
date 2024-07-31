import cv2
import numpy as np
import supervision as sv
from ultralytics import YOLO
import time
import logging
logging.basicConfig(level=logging.ERROR)

model = YOLO("yolov8n.pt")
tracker = sv.ByteTrack()
box_annotator = sv.BoundingBoxAnnotator()
label_annotator = sv.LabelAnnotator()
trace_annotator = sv.TraceAnnotator()

# Initialize recording state and start time
is_recording = False
start_time = 0
record_duration = 20  # seconds

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

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

camera = cv2.VideoCapture(0)  # 0 is usually the default camera

while True:
    ret, frame = camera.read()
    if not ret:
        print("Failed to grab frame")
        break

    processed_frame = callback(frame, 0)

    # Check if objects were detected
    if len(sv.Detections.from_ultralytics(model(frame)[0])) > 0:
        if not is_recording:
            is_recording = True
            start_time = time.time()
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
    cv2.imshow('Processed Frame', processed_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
        break

camera.release()
out.release()
cv2.destroyAllWindows()