https://github.com/olawalejuwonm/AnomalyDetector?tab=readme-ov-file#how-to-obtain-telegram-bot-token-and-chat-id

# Anomaly Detector

## Overview

Anomaly Detector is a Flask-based application designed to detect anomalies in video streams. The application captures video frames, processes them, and identifies any anomalies based on predefined criteria.

## Features

- Real-time video capture and processing
- Anomaly detection using custom algorithms
- REST API for starting video recording on connected device
- Metadata storage for recorded videos


## Usage

### Software Installation

### Local Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/olawalejuwonm/AnomalyDetector.git
    cd AnomalyDetector
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    venv\Scripts\activate  # On Windows
    # source venv/bin/activate  # On macOS/Linux
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Start the Flask application:
    ```sh
    python app.py
    ```


### How to obtain Telegram Bot Token and Chat/Group ID

To obtain a Telegram Bot Token and Chat ID for the Surveillance System, follow these steps:

1. Search for "BotFather" in Telegram or visit [https://t.me/botfather](https://t.me/botfather).
2. Click the start button to initiate interaction with BotFather.
3. Type `/newbot` and follow the instructions to create a new bot, providing a name and username when prompted.
4. Upon successful creation, you will receive a message containing a link to access the bot and a bot token. Save the bot token, as it will be needed for the Surveillance System to interact with the bot.
5. To ensure that only authorized users can interact with the Telegram bot, restrict message handling to a specific user ID. Set the chat ID of the Telegram group as the authorized user ID.
6. To find the chat ID of the group, use [t.me/myidbot](https://t.me/myidbot) to converse with IDBot. Add IDBot to the Telegram chat created and type `/getgroupid@myidbot` to obtain the chat ID of the group.



Remember, setting the authorized chat ID is necessary to prevent unauthorized users from sending commands to the bot.

P.S:  If you enjoyed using this software, please leave a STAR on the repository. It will help others find the repository and encourage me to continue working on it.
 
## API Endpoints


- `POST /run-main`: Runs the [`main.py`]("main.py") script.

## Configuration

You can configure various parameters in the `config.py` file, such as:
- Video save directory
- Recording duration
- Anomaly detection thresholds

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

<!-- ## License

This project is licensed under the MIT License. See the LICENSE file for details. -->

## Acknowledgements

- [OpenCV](https://opencv.org/) for video processing
- [Flask](https://flask.palletsprojects.com/) for the web framework


# Initialize the frame count for the last detected movement
last_movement_frame_count = 0

        if "detections" in metadata and any(
            metadata["detections"].get(int(tracker_id), {}).get("previous_position")
            is not None
            and metadata["detections"][int(tracker_id)]["previous_position"]
            != bbox.tolist()
            for tracker_id, bbox in zip(
                detected_objects.tracker_id, detected_objects.xyxy
            )
        ):
            last_movement_frame_count = frame_count


        else:
            if is_recording:
                elapsed_time_since_movement = (
                    frame_count - last_movement_frame_count
                ) / frame_rate
                if elapsed_time_since_movement >= 3:
                    is_recording = False  # Stop recording
                    # Use a separate thread to release the video and write metadata
                    threading.Thread(
                        target=release_video,
                        args=(
                            out,
                            metadata,
                            start_time,
                            record_duration,
                            video_directory,
                        ),
                    ).start()




{0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 5: 'bus', 6: 'train', 7: 'truck', 8: 'boat', 9: 'traffic light', 10: 'fire hydrant', 11: 'stop sign', 12: 'parking meter', 13: 'bench', 14: 'bird', 15: 'cat', 16: 'dog', 17: 'horse', 18: 'sheep', 19: 'cow', 20: 'elephant', 21: 'bear', 22: 'zebra', 23: 'giraffe', 24: 'backpack', 25: 'umbrella', 26: 'handbag', 27: 'tie', 28: 'suitcase', 29: 'frisbee', 30: 'skis', 31: 'snowboard', 32: 'sports ball', 33: 'kite', 34: 'baseball bat', 35: 'baseball glove', 36: 'skateboard', 37: 'surfboard', 38: 'tennis racket', 39: 'bottle', 40: 'wine glass', 41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl', 46: 'banana', 47: 'apple', 48: 'sandwich', 49: 'orange', 50: 'broccoli', 51: 'carrot', 52: 'hot dog', 53: 'pizza', 54: 'donut', 55: 'cake', 56: 'chair', 57: 'couch', 58: 'potted plant', 59: 'bed', 60: 'dining table', 61: 'toilet', 62: 'tv', 63: 'laptop', 64: 'mouse', 65: 'remote', 66: 'keyboard', 67: 'cell phone', 68: 'microwave', 69: 'oven', 70: 'toaster', 71: 'sink', 72: 'refrigerator', 73: 'book', 74: 'clock', 75: 'vase', 76: 'scissors', 77: 'teddy bear', 78: 'hair drier', 79: 'toothbrush'}