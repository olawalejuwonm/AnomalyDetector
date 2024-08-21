from flask import Flask, render_template, jsonify
import os
import json

app = Flask(__name__)


@app.route("/")
def video_gallery():
    video_directory = os.path.join(app.static_folder, "recorded_videos")  # Updated path
    video_directory = os.path.join(app.static_folder, "recorded_videos")
    video_files = [f for f in os.listdir(video_directory) if f.endswith(".webm")]

    video_metadata = []
    for video_file in video_files:
        metadata_file = os.path.join(video_directory, f"{video_file}.json")
        if os.path.exists(metadata_file):
            with open(metadata_file, "r") as f:
                metadata = json.load(f)
            video_metadata.append({"file_name": video_file, "metadata": metadata})
        else:
            video_metadata.append({"file_name": video_file, "metadata": None})

    return render_template("video_gallery.html", videos=video_metadata)


@app.route("/check-videos")
def check_videos():
    video_directory = os.path.join(app.static_folder, "recorded_videos")
    video_files = [f for f in os.listdir(video_directory) if f.endswith(".webm")]
    return jsonify(video_files)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
