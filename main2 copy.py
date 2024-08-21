import cv2  # Import the OpenCV library for computer vision tasks
import numpy as np  # Import the NumPy library for numerical operations
import supervision as sv  # Import the supervision library for tracking and annotation
from ultralytics import YOLO  # Import the YOLO model from the ultralytics library
import requests  # Import the requests library for making HTTP requests
import os  # Import the os module for interacting with the operating system
import datetime  # Import the datetime module for date and time operations

model = YOLO("yolov8n.pt")  # Load the YOLO model with the specified weights
tracker = sv.ByteTrack()  # Initialize the ByteTrack tracker
box_annotator = (
    sv.BoxAnnotator()
)  # Initialize the BoxAnnotator for drawing bounding boxes
label_annotator = (
    sv.LabelAnnotator()
)  # Initialize the LabelAnnotator for drawing labels
trace_annotator = (
    sv.TraceAnnotator()
)  # Initialize the TraceAnnotator for drawing traces


def callback(frame: np.ndarray) -> np.ndarray:
    results = model(frame)[0]  # Run the YOLO model on the frame and get the results
    detections = sv.Detections.from_ultralytics(
        results
    )  # Convert results to Detections object
    detections = tracker.update_with_detections(
        detections
    )  # Update tracker with detections

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
    return (
        detections,
        annotated_frame,
    )  # Return detections and processed frame # Annotate frame with traces


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


bot_token = "7063368407:AAHFXUgXDZBw4LkC4q-jLkBNgwJxQ2qw4yw"  # Telegram bot token
chat_id = "-1002043489442"  # Telegram chat ID
camera = cv2.VideoCapture(0)  # Open the default camera
is_recording = False  # Initialize recording state
start_time = 0  # Initialize start time
record_duration = 20  # Set recording duration to 20 seconds

video_directory = "static/recorded_videos"  # Directory path for recorded videos

if not os.path.exists(video_directory):
    os.makedirs(video_directory)  # Create the directory if it doesn't exist

fourcc = cv2.VideoWriter_fourcc(*"VP90")  # Define the codec for WebM format
out = None  # Initialize the VideoWriter object


def start_new_recording():
    output_file = f'output_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.webm'  # Output file name
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

    # detected_objects = sv.Detections.from_ultralytics(
    #     model(frame)[0]
    # )  # Get detections from the model

    if len(detected_objects) > 0:
        if not is_recording:
            is_recording = True  # Start recording
            out = start_new_recording()  # Start a new recording with a new timestamp
            class_ids = detected_objects.class_id  # Get class IDs of detected objects
            object_names = [
                model.names[class_id] for class_id in class_ids
            ]  # Get names of detected objects
            message = f"Object detected! Starting recording. Detected objects: {', '.join(object_names)}."  # Create message
            send_telegram_message(bot_token, chat_id, message)  # Send the message
    else:
        if is_recording:
            is_recording = False  # Stop recording
            out.release()  # Release the VideoWriter object

    if is_recording:
        out.write(processed_frame)  # Write the processed frame to the output file

    cv2.imshow("Processed Frame", processed_frame)  # Display the processed frame

    if cv2.waitKey(1) & 0xFF == ord("q"):  # Press 'q' to quit
        break

camera.release()  # Release the camera
if is_recording:
    out.release()  # Release the VideoWriter object
cv2.destroyAllWindows()  # Close all OpenCV windows
