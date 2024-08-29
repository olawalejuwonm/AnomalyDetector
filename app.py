from flask import (
    Flask,
    render_template,
    jsonify,
    request,
)  # Import necessary Flask modules
import os  # Import os module for interacting with the operating system
import json  # Import json module for handling JSON data
import sys  # Import sys module to get the path to the current Python interpreter
import subprocess  # Import subprocess module for running external scripts
import threading  # Import threading module to handle concurrent execution
from flaskwebgui import FlaskUI  # Import FlaskUI from flaskwebgui
from dotenv import load_dotenv  # for enviromental variables
from mainmodule import SurveillanceSystem  # Import the SurveillanceSystem class from mainmodule.py


# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)  # Create a Flask application instance

# Enable template auto-reloading
app.config["TEMPLATES_AUTO_RELOAD"] = True


def get_video_files():
    video_directory = os.path.join(
        app.static_folder, "recorded_videos"
    )  # Define the path to the video directory
    if not os.path.exists(video_directory):
        os.makedirs(video_directory)  # Create the directory if it doesn't exist

    video_files = [
        f
        for f in os.listdir(video_directory)
        if f.endswith(".webm")
        and os.path.exists(
            os.path.join(video_directory, f"{f}.json")
        )
    ]
    return video_directory, video_files  # Return the video directory and files


@app.route("/")  # Define route for the root URL
def video_gallery():
    video_directory, video_files = get_video_files()  # Get the list of video files

    video_metadata = []  # Initialize an empty list to store video metadata
    for video_file in video_files:  # Iterate over each video file
        metadata_file = os.path.join(
            video_directory, f"{video_file}.json"
        )  # Define the path to the metadata file
        if os.path.exists(metadata_file):  # Check if the metadata file exists
            with open(metadata_file, "r") as f:  # Open the metadata file
                metadata = json.load(f)  # Load the metadata from the file
            video_metadata.append(
                {"file_name": video_file, "metadata": metadata}
            )  # Append the video file and its metadata to the list
        else:
            video_metadata.append(
                {"file_name": video_file, "metadata": None}
            )  # Append the video file with no metadata
    # reverse operation on the video_metadata list to display the most recent videos first
    video_metadata = video_metadata[::-1]
    return render_template(
        "video_gallery.html", videos=video_metadata
    )  # Render the video gallery template with the video metadata


@app.route("/check-videos")  # Define route for checking available videos
def check_videos():
    _, video_files = get_video_files()  # Get the list of video files

    return jsonify(video_files)  # Return the list of video files as JSON


@app.route(
    "/delete-video", methods=["POST"]
)  # Define route for deleting a video, only allow POST requests
def delete_video():
    data = request.get_json()  # Get the JSON data from the request
    video_file = data.get("file_name")  # Extract the video file name from the data

    if not video_file:  # Check if the video file name is provided
        return (
            jsonify({"error": "No video file specified"}),
            400,
        )  # Return an error if not provided

    video_path = os.path.join(
        app.static_folder, "recorded_videos", video_file
    )  # Define the path to the video file
    metadata_path = os.path.join(
        app.static_folder, "recorded_videos", f"{video_file}.json"
    )  # Define the path to the metadata file

    if os.path.exists(video_path):  # Check if the video file exists
        os.remove(video_path)  # Remove the video file
        if os.path.exists(metadata_path):  # Check if the metadata file exists
            os.remove(metadata_path)  # Remove the metadata file
        return jsonify(
            {"success": f"{video_file} deleted successfully"}
        )  # Return success message
    else:
        return (
            jsonify({"error": "Video file not found"}),
            404,
        )  # Return error if the video file is not found


# Global variable to track if the script is running
is_running = False
lock = threading.Lock()  # Lock to ensure thread-safe access to the is_running variable


@app.route("/run-main", methods=["POST"])  # Define route to run main.py
def run_main():
    global is_running
    with lock:
        if is_running:
            return jsonify(
                {"error": "Kindly wait... The surveillance system is already running."}
            )  # Return error if script is already running
        is_running = True

    try:
        # Create an instance of the SurveillanceSystem class
        system = SurveillanceSystem()

        # Function to run the surveillance system and capture output
        def run_system():
            try:
                system.run()
            except Exception as e:
                print(f"Error: {e}")

        # Run the surveillance system in a separate thread
        thread = threading.Thread(target=run_system)
        thread.start()

        return jsonify({"output": "Surveillance system started successfully."})  # Return success message
    except Exception as e:
        return jsonify({"error": str(e)})  # Return any exception as JSON
    finally:
        with lock:
            is_running = False  # Reset the running state


# Used code from https://pypi.org/project/flaskwebgui/ (Advanced Usage)
def start_flask(**server_kwargs):

    app = server_kwargs.pop("app", None)
    server_kwargs.pop("debug", None)

    try:
        import waitress

        waitress.serve(app, **server_kwargs)
    except Exception as e:
        print(f"Error occurred: {e}")
        app.run(**server_kwargs)


if __name__ == "__main__":  # Check if the script is run directly

    if os.getenv("ENVIRONMENT") != "production":
        app.run(
        host="0.0.0.0", debug=True, port=5000
        )  # Run the Flask application on the local network
    else:
        FlaskUI(
            server=start_flask,
            server_kwargs={
                "app": app,
                "port": 5000,
                "host": "0.0.0.0",
                # "threaded": True,
            },
            width=800,
            height=600,
        ).run()  # Run the Flask application using FlaskUI
