from flask import Flask, render_template, jsonify, request
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

@app.route('/delete-video', methods=['POST'])
def delete_video():
    data = request.get_json()
    video_file = data.get('file_name')
    
    if not video_file:
        return jsonify({'error': 'No video file specified'}), 400
    
    video_path = os.path.join(app.static_folder, 'recorded_videos', video_file)
    metadata_path = os.path.join(app.static_folder, 'recorded_videos', f'{video_file}.json')
    
    if os.path.exists(video_path):
        os.remove(video_path)
        if os.path.exists(metadata_path):
            os.remove(metadata_path)
        return jsonify({'success': f'{video_file} deleted successfully'})
    else:
        return jsonify({'error': 'Video file not found'}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
