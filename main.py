import mimetypes
import cv2  # Import the OpenCV library for computer vision tasks
import numpy as np  # Import the NumPy library for numerical operations
import supervision as sv  # Import the supervision library for tracking and annotation
from ultralytics import YOLO  # Import the YOLO model from the ultralytics library
import os  # Import the os module for interacting with the operating system
import datetime  # Import the datetime module for date and time operations
import json  # Import the json module for handling JSON data
import threading  # to handle concurrent execution
from dotenv import load_dotenv  # for enviromental variables
import http.client
import concurrent.futures

# Load environment variables from .env file
load_dotenv()


class SurveillanceSystem:
    def __init__(
        self,
        bot_token=None,
        chat_id=None,
        environment="development",
        send_recording=False,
        model="yolov8n.pt",
        camera_port=0,
    ):
        print("Initializing the Intelligent Surveillance System")
        print("Initial configuration:")
        print(f"Environment: {environment}")
        print(f"Model: {model}")
        print(f"Camera Port: {camera_port}")
    
        self.model = YOLO(
            model,  # Load the YOLO model with the specified weights
            # device="cuda" if torch.cuda.is_available() else "cpu",
        )  # Load the YOLO model with the specified weights
        self.tracker = sv.ByteTrack()  # Initialize the ByteTrack tracker
        self.box_annotator = (
            sv.BoxAnnotator()
        )  # Initialize the BoxAnnotator for drawing bounding boxes
        self.label_annotator = (
            sv.LabelAnnotator()
        )  # Initialize the LabelAnnotator for drawing labels
        self.trace_annotator = (
            sv.TraceAnnotator()
        )  # Initialize the TraceAnnotator for drawing traces
        self.bot_token = bot_token or os.getenv(
            "TELEGRAM_BOT_TOKEN"
        )  # Telegram bot token
        self.chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID")  # Telegram chat ID
        self.environment = environment or os.getenv("ENVIRONMENT")  # Environment
        self.send_recording = send_recording  # For sending recorded video to telegram
        self.camera = cv2.VideoCapture(camera_port)  # Open the default camera
        self.is_recording = False  # Initialize recording state
        self.start_time = 0  # Initialize start time
        self.record_duration = 20  # Set recording duration to 20 seconds
        self.video_directory = (
            "static/recorded_videos"  # Directory path for recorded videos
        )
        self.fourcc = cv2.VideoWriter_fourcc(
            *"VP90"
        )  # Define the codec for WebM format
        self.out = None  # Initialize the VideoWriter object
        self.metadata = {}  # Initialize metadata dictionary
        self.frame_count = 0  # Initialize frame counter
        self.frame_rate = 20.0  # Frame rate of the video

        # print(self.bot_token, self.chat_id)

        if not os.path.exists(self.video_directory):
            os.makedirs(
                self.video_directory
            )  # Create the directory if it doesn't exist

        if not self.bot_token or not self.chat_id:
            raise ValueError(
                "Please set the TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables."
            )

    def callback(self, frame: np.ndarray) -> tuple:
        results = self.model(frame)[
            0
        ]  # Run the YOLO model on the frame and get the results
        detections = sv.Detections.from_ultralytics(
            results
        )  # Convert results to Detections object
        detections = self.tracker.update_with_detections(
            detections
        )  # Update tracker with detections

        labels = [
            f"#{tracker_id} {results.names[class_id]}"
            for class_id, tracker_id in zip(detections.class_id, detections.tracker_id)
        ]  # Create labels for each detection

        annotated_frame = self.box_annotator.annotate(
            frame.copy(), detections=detections
        )  # Annotate frame with bounding boxes
        annotated_frame = self.label_annotator.annotate(
            annotated_frame, detections=detections, labels=labels
        )  # Annotate frame with labels
        return detections, annotated_frame  # Return detections and processed frame

    def send_telegram_message(self, message):
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            payload = {"chat_id": self.chat_id, "text": message}
            headers = {"Content-Type": "application/json"}
            conn = http.client.HTTPSConnection("api.telegram.org")
            conn.request("POST", url, body=json.dumps(payload), headers=headers)
            response = conn.getresponse()
            response_data = response.read().decode("utf-8")
            conn.close()

            if response.status != 200:
                print(response_data)
                raise ValueError(f"Failed to send message: {response.status}")

            return json.loads(response_data)
        except Exception as e:
            print(f"Error sending message: {e}")

    def send_telegram_frame(self, frame, filename="frame.jpg"):
        """
        Sends a processed frame to a Telegram chat.

        Parameters:
        - frame (np.ndarray): The processed frame to send.
        - filename (str): The filename to save the frame as.

        Returns:
        - response (dict): The response from the Telegram API.
        """
        try:
            # Convert frame to image and save
            cv2.imwrite(filename, frame)

            # Prepare the multipart/form-data payload
            boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
            payload = (
                f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="chat_id"\r\n\r\n{self.chat_id}\r\n'
                f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="photo"; filename="{filename}"\r\n'
                f"Content-Type: {mimetypes.guess_type(filename)[0]}\r\n\r\n"
            )

            with open(filename, "rb") as f:
                file_data = f.read()

            payload += file_data.decode("latin1")
            payload += f"\r\n--{boundary}--\r\n"

            headers = {
                "Content-Type": f"multipart/form-data; boundary={boundary}",
                "Content-Length": str(len(payload)),
            }

            # Send the image to Telegram
            conn = http.client.HTTPSConnection("api.telegram.org")
            conn.request(
                "POST", f"/bot{self.bot_token}/sendPhoto", body=payload, headers=headers
            )
            response = conn.getresponse()
            response_data = response.read().decode("utf-8")
            conn.close()

            if response.status != 200:
                raise ValueError(f"Failed to send frame: {response.status}")

            return json.loads(response_data)
        except Exception as e:
            print(f"Error sending frame: {e}")

    def send_telegram_video(self, video_path, filename="video.webm"):
        """
        Sends a video to a Telegram chat.

        Parameters:
        - video_path (str): The path to the video file to send.
        - filename (str): The filename to save the video as.

        Returns:
        - response (dict): The response from the Telegram API.
        """
        try:
            # Prepare the multipart/form-data payload
            boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
            payload = (
                f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="chat_id"\r\n\r\n{self.chat_id}\r\n'
                f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="video"; filename="{filename}"\r\n'
                f"Content-Type: {mimetypes.guess_type(filename)[0]}\r\n\r\n"
            )

            with open(video_path, "rb") as f:
                file_data = f.read()

            payload += file_data.decode("latin1")
            payload += f"\r\n--{boundary}--\r\n"

            headers = {
                "Content-Type": f"multipart/form-data; boundary={boundary}",
                "Content-Length": str(len(payload)),
            }

            # Send the video to Telegram
            conn = http.client.HTTPSConnection("api.telegram.org")
            conn.request(
                "POST", f"/bot{self.bot_token}/sendVideo", body=payload, headers=headers
            )
            response = conn.getresponse()
            response_data = response.read().decode("utf-8")
            conn.close()

            if response.status != 200:
                raise ValueError(f"Failed to send video: {response.status}")

            return json.loads(response_data)
        except Exception as e:
            print(f"Error sending video: {e}")

    def run_telegram_tasks_in_thread(self, message, processed_frame):
        def task():
            self.send_telegram_message(message)
            self.send_telegram_frame(processed_frame)

        executor = concurrent.futures.ThreadPoolExecutor()
        executor.submit(task)

    def write_metadata_to_file(self):
        """
        Writes metadata to a file.
        """
        self.metadata["end_time"] = datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        self.metadata["total_duration"] = min(
            (self.frame_count / self.frame_rate), self.record_duration
        )
        metadata_file = os.path.join(
            self.video_directory, f'{self.metadata["file_name"]}.json'
        )
        with open(metadata_file, "w") as f:
            json.dump(self.metadata, f, indent=4)

    def release_video(self):
        self.out.release()  # Release the VideoWriter object
        self.write_metadata_to_file()  # Write metadata to a file
        if self.send_recording:
            self.send_telegram_video(
                os.path.join(self.video_directory, self.metadata["file_name"]),
                filename=self.metadata["file_name"],
            )  # Send the recorded video to Telegram

    def start_new_recording(self):
        output_file = f'output_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.webm'  # Output file name
        self.metadata["file_name"] = output_file  # Add file name to metadata
        self.metadata["detections"] = {}  # Initialize detections dictionary in metadata
        self.metadata["start_time"] = datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )  # Add start time to metadata
        self.out = cv2.VideoWriter(
            os.path.join(self.video_directory, output_file),
            self.fourcc,
            self.frame_rate,
            (int(self.camera.get(3)), int(self.camera.get(4))),
        )  # Create VideoWriter object

    def process_frame(self, frame):
        detected_objects, processed_frame = self.callback(
            frame
        )  # Process the frame using the callback function
        if len(detected_objects) > 0:
            if not self.is_recording:
                self.is_recording = True  # Start recording
                self.start_time = datetime.datetime.now()  # Record the start time
                self.start_new_recording()  # Start a new recording with a new timestamp
                self.frame_count = 0  # Reset frame counter
                class_ids = (
                    detected_objects.class_id
                )  # Get class IDs of detected objects
                object_names = [
                    self.model.names[class_id] for class_id in class_ids
                ]  # Get names of detected objects
                object_count = len(object_names)  # Count the number of detected objects
                object_word = (
                    "object" if object_count < 2 else "objects"
                )  # Singular or plural
                message = f"The Surveillance System has detected {object_count} {object_word} and started recording. {object_word} detected: {', '.join(object_names)}."  # Create message
                # Run the tasks in a separate thread
                self.run_telegram_tasks_in_thread(message, processed_frame)

            # Update metadata with detected objects
            for class_id, tracker_id, bbox in zip(
                detected_objects.class_id,
                detected_objects.tracker_id,
                detected_objects.xyxy,
            ):
                tracker_id = int(
                    tracker_id
                )  # Ensure tracker_id is a standard Python int
                if tracker_id not in self.metadata["detections"]:
                    self.metadata["detections"][tracker_id] = {
                        "class_id": int(
                            class_id
                        ),  # Ensure class_id is a standard Python int
                        "class_name": self.model.names[class_id],
                        "positions": [],
                        "previous_position": None,  # Initialize previous position
                    }

                # Get the current bounding box
                current_bbox = bbox.tolist()

                # Determine the movement direction
                movement_direction = "stationary"
                if (
                    self.metadata["detections"][tracker_id]["previous_position"]
                    is not None
                ):
                    previous_bbox = self.metadata["detections"][tracker_id][
                        "previous_position"
                    ]
                    if current_bbox[0] > previous_bbox[0]:
                        movement_direction = "right"
                    elif current_bbox[0] < previous_bbox[0]:
                        movement_direction = "left"

                # Update the metadata with the current position and movement direction
                self.metadata["detections"][tracker_id]["positions"].append(
                    {
                        "bbox": current_bbox,
                        "timestamp": datetime.datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        "movement_direction": movement_direction,
                    }
                )

                # Update the previous position
                self.metadata["detections"][tracker_id][
                    "previous_position"
                ] = current_bbox
        else:
            if self.is_recording:
                self.is_recording = False  # Stop recording
                # Use a separate thread to release the video and write metadata
                threading.Thread(target=self.release_video).start()
        if self.is_recording:
            elapsed_time = self.frame_count / self.frame_rate  # Calculate elapsed time
            print(f"Elapsed Time: {elapsed_time}s")  # Print elapsed time
            if elapsed_time >= self.record_duration:
                self.is_recording = False  # Stop recording
                # Use a separate thread to release the video and write metadata
                threading.Thread(target=self.release_video).start()
            else:
                self.out.write(
                    processed_frame
                )  # Write the processed frame to the output file
                self.frame_count += 1  # Increment frame counter

        return processed_frame

    # def get_cameras(self):
    #     cameras = []
    #     for i in range(10):
    #         camera = cv2.VideoCapture(i)
    #         if camera.isOpened():
    #             cameras.append(i)
    #             camera.release()
    #     return cameras

    # get camera connected to the system with their name and status
    def get_cameras(self):
        def list_ports():
            """
            Test the ports and returns a tuple with the available ports and the ones that are working.
            """
            non_working_ports = []
            dev_port = 0
            working_ports = []
            available_ports = []
            while (
                len(non_working_ports) < 6
            ):  # if there are more than 5 non working ports stop the testing.
                camera = cv2.VideoCapture(dev_port)
                if not camera.isOpened():
                    non_working_ports.append(dev_port)
                    print("Port %s is not working." % dev_port)
                else:
                    is_reading, img = camera.read()
                    w = camera.get(3)
                    h = camera.get(4)
                    if is_reading:
                        print(
                            "Port %s is working and reads images (%s x %s)"
                            % (dev_port, h, w)
                        )
                        working_ports.append(dev_port)
                    else:
                        print(
                            "Port %s for camera ( %s x %s) is present but does not reads."
                            % (dev_port, h, w)
                        )
                        available_ports.append(dev_port)
                dev_port += 1
            return available_ports, working_ports, non_working_ports

        cameras = []
        cameras = list_ports()
        # return working ports camera as dict with id and name
        return {"cameras": [{"id": i, "name": f"Camera {i+1}"} for i in cameras[1]]}

    def run(self):
        print("Running the Intelligent Surveillance System")

        while True:
            ret, frame = self.camera.read()  # Read a frame from the camera
            if not ret:
                print(
                    "Failed to grab frame"
                )  # Print error message if frame is not grabbed
                break

            processed_frame = self.process_frame(frame)  # Process the frame
            cv2.imshow(
                "Intelligent Surveillance System (Press Q to Quit)", processed_frame
            )  # Display the processed frame

            if cv2.waitKey(1) & 0xFF == ord("q"):  # Press 'q' to quit
                break

        self.camera.release()  # Release the camera
        if self.is_recording:
            threading.Thread(target=self.release_video).start()
        cv2.destroyAllWindows()  # Close all OpenCV windows


def main():
    system = SurveillanceSystem()
    system.run()


if __name__ == "__main__":
    main()
