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

2. Use the provided REST API to control the video recording:
    - Start recording:
        ```sh
        curl -X POST http://localhost:5000/start-recording
        ```
    - Stop recording:
        ```sh
        curl -X POST http://localhost:5000/stop-recording
        ```

3. The recorded videos and metadata will be saved in the specified directory.

## API Endpoints

- `POST /start-recording`: Starts the video recording.
- `POST /stop-recording`: Stops the video recording.
- `POST /run-main`: Runs the [`main.py`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fc%3A%2FUsers%2FHP%2FDocuments%2FGitHub%2FUoL-Projects%2FAnomalyDetector%2Fmain.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "c:\Users\HP\Documents\GitHub\UoL-Projects\AnomalyDetector\main.py") script.

## Configuration

You can configure various parameters in the `config.py` file, such as:
- Video save directory
- Recording duration
- Anomaly detection thresholds

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements

- [OpenCV](https://opencv.org/) for video processing
- [Flask](https://flask.palletsprojects.com/) for the web framework
