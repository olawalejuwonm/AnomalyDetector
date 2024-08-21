import cv2  # Import the OpenCV library for computer vision tasks
import numpy as np  # Import the NumPy library for numerical operations
import supervision as sv  # Import the supervision library for tracking and annotation
from ultralytics import YOLO  # Import the YOLO model from the ultralytics library
import requests  # Import the requests library for making HTTP requests
import os  # Import the os module for interacting with the operating system
import datetime  # Import the datetime module for date and time operations
import json  # Import the json module for handling JSON data

model = YOLO("yolov8n.pt")  # Load the YOLO model with the specified weights
tracker = sv.ByteTrack()  # Initialize the ByteTrack tracker
box_annotator = sv.BoxAnnotator()  # Initialize the BoxAnnotator for drawing bounding boxes
label_annotator = sv.LabelAnnotator()  # Initialize the LabelAnnotator for drawing labels
trace_annotator = sv.TraceAnnotator()  # Initialize the TraceAnnotator for drawing traces

def callback(frame: np.ndarray) -> tuple:
    results = model(frame)[0]  # Run the YOLO model on the frame and get the results
    detections = sv.Detections.from_ultralytics(results)  # Convert results to Detections object
    detections = tracker.update_with_detections(detections)  # Update tracker with detections

    labels = [
        f"#{tracker_id} {results.names[class_id]}"
        for class_id, tracker_id in zip(detections.class_id, detections.tracker_id)
    ]  # Create labels for each detection

    annotated_frame = box_annotator.annotate(
        frame.copy(), detections=detections
    )  # Annotate frame with bounding boxes
    annotated_frame = label_annotator.annotate(
        annotated_frame, detections=detections, labels=labels
    )  # Annotate frame with labels
    return detections, annotated_frame  # Return detections and processed frame

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
    send_message_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"  # URL for sending messages
    payload = {"chat_id": chat_id, "text": message}  # Payload for the POST request
    response = requests.post(send_message_url, data=payload)  # Send the POST request
    return response.json()  # Return the response as JSON

bot_token = "YOUR_BOT_TOKEN"  # Telegram bot token
chat_id = "YOUR_CHAT_ID"  # Telegram chat ID
camera = cv2.VideoCapture(0)  # Open the default camera
is_recording = False  # Initialize recording state
start_time = 0  # Initialize start time
record_duration = 20  # Set recording duration to 20 seconds

video_directory = "static/recorded_videos"  # Directory path for recorded videos

if not os.path.exists(video_directory):
    os.makedirs(video_directory)  # Create the directory if it doesn't exist

fourcc = cv2.VideoWriter_fourcc(*"VP90")  # Define the codec for WebM format
out = None  # Initialize the VideoWriter object
metadata = {}  # Initialize metadata dictionary

def start_new_recording():
    output_file = f'output_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.webm'  # Output file name
    metadata['file_name'] = output_file  # Add file name to metadata
    metadata['detections'] = {}  # Initialize detections dictionary in metadata
    return cv2.VideoWriter(
        os.path.join(video_directory, output_file),
        fourcc,
        20.0,
        (int(camera.get(3)), int(camera.get(4))),
    )  # Create VideoWriter object

while True:
    ret, frame = camera.read()  # Read a frame from the camera
    if not ret:
        print("Failed to grab frame")  # Print error message if frame is not grabbed
        break

    detected_objects, processed_frame = callback(frame)  # Process the frame using the callback function

    if len(detected_objects) > 0:
        if not is_recording:
            is_recording = True  # Start recording
            start_time = datetime.datetime.now()  # Record the start time
            out = start_new_recording()  # Start a new recording with a new timestamp
            class_ids = detected_objects.class_id  # Get class IDs of detected objects
            object_names = [model.names[class_id] for class_id in class_ids]  # Get names of detected objects
            message = f"Object detected! Starting recording. Detected objects: {', '.join(object_names)}."  # Create message
            send_telegram_message(bot_token, chat_id, message)  # Send the message
        # Update metadata with detected objects
        for class_id, tracker_id, bbox in zip(detected_objects.class_id, detected_objects.tracker_id, detected_objects.xyxy):
            tracker_id = int(tracker_id)  # Ensure tracker_id is a standard Python int
            if tracker_id not in metadata['detections']:
                metadata['detections'][tracker_id] = {
                    'class_id': int(class_id),  # Ensure class_id is a standard Python int
                    'class_name': model.names[class_id],
                    'positions': [],
                    'previous_position': None  # Initialize previous position
                }

            # Get the current bounding box
            current_bbox = bbox.tolist()

            # Determine the movement direction
            movement_direction = "stationary"
            if metadata['detections'][tracker_id]['previous_position'] is not None:
                previous_bbox = metadata['detections'][tracker_id]['previous_position']
                if current_bbox[0] > previous_bbox[0]:
                    movement_direction = "right"
                elif current_bbox[0] < previous_bbox[0]:
                    movement_direction = "left"

            # Update the metadata with the current position and movement direction
            metadata['detections'][tracker_id]['positions'].append({
                'bbox': current_bbox,
                'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'movement_direction': movement_direction
            })

            # Update the previous position
            metadata['detections'][tracker_id]['previous_position'] = current_bbox
    else:
        if is_recording:
            is_recording = False  # Stop recording
            out.release()  # Release the VideoWriter object
            # Write metadata to a file
            metadata_file = os.path.join(video_directory, f'{metadata["file_name"]}.json')
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=4)

    if is_recording:
        elapsed_time = (datetime.datetime.now() - start_time).total_seconds()
        if elapsed_time > record_duration:
            is_recording = False  # Stop recording
            out.release()  # Release the VideoWriter object
            # Write metadata to a file
            metadata_file = os.path.join(video_directory, f'{metadata["file_name"]}.json')
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=4)
        else:
            out.write(processed_frame)  # Write the processed frame to the output file

    cv2.imshow("Processed Frame", processed_frame)  # Display the processed frame

    if cv2.waitKey(1) & 0xFF == ord("q"):  # Press 'q' to quit
        break

camera.release()  # Release the camera
if is_recording:
    out.release()  # Release the VideoWriter object
    # Write metadata to a file if recording was active
    metadata_file = os.path.join(video_directory, f'{metadata["file_name"]}.json')
    with open(metadata_file, 'w') as f:
        print(metadata)
        json.dump(metadata, f, indent=4)
cv2.destroyAllWindows()  # Close all OpenCV windows