from imageai.Detection import VideoObjectDetection
import os
import cv2

execution_path = os.getcwd()


camera = cv2.VideoCapture(0)

detector = VideoObjectDetection()
detector.setModelTypeAsTinyYOLOv3()
detector.setModelPath(os.path.join(execution_path , "tiny-yolov3.pt"))
detector.loadModel()


video_path = detector.detectObjectsFromVideo(
                camera_input=camera,
                return_detected_frame = True,
                save_detected_video=True,
                output_file_path=os.path.join(execution_path, "camera_detected_video"),
                frames_per_second=20, log_progress=True, minimum_percentage_probability=40)
# Display the resulting frame
cv2.imshow('frame', video_path)