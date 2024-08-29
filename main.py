import os  # Import the os module for interacting with the operating system
import datetime  # Import the datetime module for date and time operations
import json  # Import the json module for handling JSON data
import threading  # to handle concurrent execution
import cv2  # Import the OpenCV library for computer vision tasks
import numpy as np  # Import the NumPy library for numerical operations
import supervision as sv  # Import the supervision library for tracking and annotation
from ultralytics import YOLO  # Import the YOLO model from the ultralytics library
import requests  # Import the requests library for making HTTP requests
from dotenv import load_dotenv  # for enviromental variables

# Load environment variables from .env file
load_dotenv()

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


def callback(frame: np.ndarray) -> tuple:
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
    try:
        send_message_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"  # URL for sending messages
        payload = {"chat_id": chat_id, "text": message}  # Payload for the POST request
        response = requests.post(
            send_message_url, data=payload
        )  # Send the POST request
        return response.json()  # Return the response as JSON
    except Exception as e:
        print(f"An error occurred sending notification: {e}")


def write_metadata_to_file(metadata, start_time, record_duration, video_directory):
    """
    Writes metadata to a file.

    Parameters:
    - metadata (dict): The metadata dictionary.
    - start_time (datetime): The start time of the recording.
    - record_duration (int): The maximum duration of the recording.
    - video_directory (str): The directory where the video and metadata files are stored.
    """
    metadata["end_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    metadata["total_duration"] = min((frame_count / frame_rate), record_duration)
    metadata_file = os.path.join(video_directory, f'{metadata["file_name"]}.json')
    with open(metadata_file, "w") as f:
        json.dump(metadata, f, indent=4)


def release_video(out, metadata, start_time, record_duration, video_directory):
    out.release()  # Release the VideoWriter object
    write_metadata_to_file(
        metadata, start_time, record_duration, video_directory
    )  # Write metadata to a file


# Read the bot token and chat ID from environment variables
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")  # Telegram bot token
chat_id = os.getenv("TELEGRAM_CHAT_ID")  # Telegram chat ID

# Ensure the environment variables are set
if not bot_token or not chat_id:
    print(
        ValueError(
            "Please set the TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables."
        )
    )

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
frame_count = 0  # Initialize frame counter
frame_rate = 20.0  # Frame rate of the video


def start_new_recording():
    output_file = f'output_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.webm'  # Output file name
    metadata["file_name"] = output_file  # Add file name to metadata
    metadata["detections"] = {}  # Initialize detections dictionary in metadata
    metadata["start_time"] = datetime.datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )  # Add start time to metadata
    return cv2.VideoWriter(
        os.path.join(video_directory, output_file),
        fourcc,
        frame_rate,
        (int(camera.get(3)), int(camera.get(4))),
    )  # Create VideoWriter object


while True:
    ret, frame = camera.read()  # Read a frame from the camera
    if not ret:
        print("Failed to grab frame")  # Print error message if frame is not grabbed
        break

    detected_objects, processed_frame = callback(
        frame
    )  # Process the frame using the callback function
    if len(detected_objects) > 0:
        if not is_recording:
            is_recording = True  # Start recording
            start_time = datetime.datetime.now()  # Record the start time
            out = start_new_recording()  # Start a new recording with a new timestamp
            frame_count = 0  # Reset frame counter
            class_ids = detected_objects.class_id  # Get class IDs of detected objects
            object_names = [
                model.names[class_id] for class_id in class_ids
            ]  # Get names of detected objects
            object_count = len(object_names)  # Count the number of detected objects
            object_word = (
                "object" if object_count < 2 else "objects"
            )  # Singular or plural
            message = f"The Surveillance System has detected {object_count} {object_word} and started recording. {object_word} detected: {', '.join(object_names)}. "  # Create message
            send_telegram_message(bot_token, chat_id, message)  # Send the message
        # Update metadata with detected objects
        for class_id, tracker_id, bbox in zip(
            detected_objects.class_id,
            detected_objects.tracker_id,
            detected_objects.xyxy,
        ):
            tracker_id = int(tracker_id)  # Ensure tracker_id is a standard Python int
            if tracker_id not in metadata["detections"]:
                metadata["detections"][tracker_id] = {
                    "class_id": int(
                        class_id
                    ),  # Ensure class_id is a standard Python int
                    "class_name": model.names[class_id],
                    "positions": [],
                    "previous_position": None,  # Initialize previous position
                }

            # Get the current bounding box
            current_bbox = bbox.tolist()

            # Determine the movement direction
            movement_direction = "stationary"
            if metadata["detections"][tracker_id]["previous_position"] is not None:
                previous_bbox = metadata["detections"][tracker_id]["previous_position"]
                if current_bbox[0] > previous_bbox[0]:
                    movement_direction = "right"
                elif current_bbox[0] < previous_bbox[0]:
                    movement_direction = "left"

            # Update the metadata with the current position and movement direction
            metadata["detections"][tracker_id]["positions"].append(
                {
                    "bbox": current_bbox,
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "movement_direction": movement_direction,
                }
            )

            # Update the previous position
            metadata["detections"][tracker_id]["previous_position"] = current_bbox
    else:
        if is_recording:
            is_recording = False  # Stop recording
            # Use a separate thread to release the video and write metadata
            threading.Thread(
                target=release_video,
                args=(out, metadata, start_time, record_duration, video_directory),
            ).start()
    if is_recording:
        elapsed_time = frame_count / frame_rate  # Calculate elapsed time
        print(f"Elapsed Time: {elapsed_time}s")  # Print elapsed time
        if elapsed_time >= record_duration:
            is_recording = False  # Stop recording
            # Use a separate thread to release the video and write metadata
            threading.Thread(
                target=release_video,
                args=(out, metadata, start_time, record_duration, video_directory),
            ).start()
        else:
            out.write(processed_frame)  # Write the processed frame to the output file
            frame_count += 1  # Increment frame counter

    cv2.imshow(
        "Surveillance System (Press Q to Quit)", processed_frame
    )  # Display the processed frame

    if cv2.waitKey(1) & 0xFF == ord("q"):  # Press 'q' to quit
        break

camera.release()  # Release the camera
if is_recording:
    out.release()  # Release the VideoWriter object
    threading.Thread(
        target=release_video,
        args=(out, metadata, start_time, record_duration, video_directory),
    ).start()
cv2.destroyAllWindows()  # Close all OpenCV windows
