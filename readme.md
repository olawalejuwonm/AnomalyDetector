[![DOI](https://zenodo.org/badge/807640991.svg)](https://zenodo.org/doi/10.5281/zenodo.13714360)

# Anomaly Detector

## Overview

Anomaly Detector is a Flask-based application designed to detect anomalies in video streams. The application captures video frames, processes them, and identifies any anomalies based on predefined criteria.

It focuses on developing indoor surveillance, leveraging advanced motion detection algorithms to enhance privacy, efficiency, and adaptability. It also addresses the limitations of traditional home security systems, which rely heavily on human monitoring and are prone to false alarms.

The proposed solution relies on local processing, using intelligent object detection to avoid the use of third-party services and improve users' privacy. It was driven by two major development iterations: the first on hardware components comprising an ESP32-CAM and a passive infrared-PIR sensor, and the second purely in software based on Supervision, Ultralytics, and YOLOv8 computer vision algorithms.

The second iteration performs better than the first concerning cost, flexibility, and adaptability by shifting from motion detection to object-focused anomaly detection. The system can operate standalone, processing real-time video and tracking object behaviour while notifying users through its web dashboard. An evaluation was conducted through user acceptance testing, accessibility testing, and performance metrics, showing the system's effectiveness in various lighting conditions and its potential for more general purposes.

Future system enhancements could include integrating hardware and software solutions for optimal performance in low-light conditions and expanding notification services.

CREDITS: [University of London](https://www.london.ac.uk/study/courses/undergraduate/bsc-computer-science)

## Features

- Real-time video capture and processing
- Anomaly detection using custom algorithms
- REST API for starting video recording on connected device
- Metadata storage for recorded videos


## Usage

### Software Installation

To install the software, please follow the instructions provided in the project releases section. This section contains the latest versions of the software, along with detailed installation guides and release notes.

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
 

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

<!-- ## License

This project is licensed under the MIT License. See the LICENSE file for details. -->

## Acknowledgements

- [OpenCV](https://opencv.org/) for video processing
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [Supervision](https://github.com/your-repo/supervision) for tracking and annotation tools
- [Ultralytics](https://ultralytics.com/) for the YOLO models
- [YOLO](https://github.com/AlexeyAB/darknet) for the object detection framework
