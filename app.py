from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def video_gallery():
    video_directory = os.path.join(app.static_folder, 'recorded_videos')  # Updated path
    video_files = [f for f in os.listdir(video_directory) if f.endswith('.webm')]
    return render_template('video_gallery.html', videos=video_files)

if __name__ == '__main__':
    app.run(debug=True)