# Anomaly Detector

## Overview

Anomaly Detector is a Flask-based application designed to detect anomalies in video streams. The application captures video frames, processes them, and identifies any anomalies based on predefined criteria.

## Features

- Real-time video capture and processing
- Anomaly detection using custom algorithms
- REST API for starting and stopping video recording
- Metadata storage for recorded videos

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/AnomalyDetector.git
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

## Usage

1. Start the Flask application:
    ```sh
    python app.py
    ```

3. The recorded videos and metadata will be saved in the specified directory.

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








{0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 5: 'bus', 6: 'train', 7: 'truck', 8: 'boat', 9: 'traffic light', 10: 'fire hydrant', 11: 'stop sign', 12: 'parking meter', 13: 'bench', 14: 'bird', 15: 'cat', 16: 'dog', 17: 'horse', 18: 'sheep', 19: 'cow', 20: 'elephant', 21: 'bear', 22: 'zebra', 23: 'giraffe', 24: 'backpack', 25: 'umbrella', 26: 'handbag', 27: 'tie', 28: 'suitcase', 29: 'frisbee', 30: 'skis', 31: 'snowboard', 32: 'sports ball', 33: 'kite', 34: 'baseball bat', 35: 'baseball glove', 36: 'skateboard', 37: 'surfboard', 38: 'tennis racket', 39: 'bottle', 40: 'wine glass', 41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl', 46: 'banana', 47: 'apple', 48: 'sandwich', 49: 'orange', 50: 'broccoli', 51: 'carrot', 52: 'hot dog', 53: 'pizza', 54: 'donut', 55: 'cake', 56: 'chair', 57: 'couch', 58: 'potted plant', 59: 'bed', 60: 'dining table', 61: 'toilet', 62: 'tv', 63: 'laptop', 64: 'mouse', 65: 'remote', 66: 'keyboard', 67: 'cell phone', 68: 'microwave', 69: 'oven', 70: 'toaster', 71: 'sink', 72: 'refrigerator', 73: 'book', 74: 'clock', 75: 'vase', 76: 'scissors', 77: 'teddy bear', 78: 'hair drier', 79: 'toothbrush'}