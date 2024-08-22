from flask import Flask, render_template, jsonify, request  # Import necessary Flask modules
import os  # Import os module for interacting with the operating system
import json  # Import json module for handling JSON data

app = Flask(__name__)  # Create a Flask application instance

@app.route("/")  # Define route for the root URL
def video_gallery():
    video_directory = os.path.join(app.static_folder, "recorded_videos")  # Define the path to the video directory
    video_files = [f for f in os.listdir(video_directory) if f.endswith(".webm")]  # List all .webm files in the directory

    video_metadata = []  # Initialize an empty list to store video metadata
    for video_file in video_files:  # Iterate over each video file
        metadata_file = os.path.join(video_directory, f"{video_file}.json")  # Define the path to the metadata file
        if os.path.exists(metadata_file):  # Check if the metadata file exists
            with open(metadata_file, "r") as f:  # Open the metadata file
                metadata = json.load(f)  # Load the metadata from the file
            video_metadata.append({"file_name": video_file, "metadata": metadata})  # Append the video file and its metadata to the list
        else:
            video_metadata.append({"file_name": video_file, "metadata": None})  # Append the video file with no metadata

    return render_template("video_gallery.html", videos=video_metadata)  # Render the video gallery template with the video metadata

@app.route("/check-videos")  # Define route for checking available videos
def check_videos():
    video_directory = os.path.join(app.static_folder, "recorded_videos")  # Define the path to the video directory
    video_files = [f for f in os.listdir(video_directory) if f.endswith(".webm")]  # List all .webm files in the directory
    return jsonify(video_files)  # Return the list of video files as JSON

@app.route('/delete-video', methods=['POST'])  # Define route for deleting a video, only allow POST requests
def delete_video():
    data = request.get_json()  # Get the JSON data from the request
    video_file = data.get('file_name')  # Extract the video file name from the data
    
    if not video_file:  # Check if the video file name is provided
        return jsonify({'error': 'No video file specified'}), 400  # Return an error if not provided
    
    video_path = os.path.join(app.static_folder, 'recorded_videos', video_file)  # Define the path to the video file
    metadata_path = os.path.join(app.static_folder, 'recorded_videos', f'{video_file}.json')  # Define the path to the metadata file
    
    if os.path.exists(video_path):  # Check if the video file exists
        os.remove(video_path)  # Remove the video file
        if os.path.exists(metadata_path):  # Check if the metadata file exists
            os.remove(metadata_path)  # Remove the metadata file
        return jsonify({'success': f'{video_file} deleted successfully'})  # Return success message
    else:
        return jsonify({'error': 'Video file not found'}), 404  # Return error if the video file is not found

if __name__ == "__main__":  # Check if the script is run directly
    app.run(host="0.0.0.0", debug=True)  # Run the Flask application with debugging enabled