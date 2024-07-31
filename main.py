# import cv2
# import os
# from imageai.Detection import ObjectDetection

# camera = cv2.VideoCapture(0)
# execution_path = os.getcwd()

# detector = ObjectDetection()
# # detector.setModelTypeAsRetinaNet()
# # detector.setModelPath(os.path.join(execution_path, "retinanet_resnet50_fpn_coco-eeacb38b.pth"))
# detector.setModelTypeAsTinyYOLOv3()
# detector.setModelPath(os.path.join(execution_path, "tiny-yolov3.pt"))
# detector.loadModel()

# while True:

#     ret, frame = camera.read()

    

#     # Check if the frame is not empty
#     if ret:
#         # Save the frame to a file
#         cv2.imwrite('output.jpg', frame)
#         detections = detector.detectObjectsFromImage(input_image='output.jpg')

#         for detection in detections:
#             print(detection["name"], " : ", detection["percentage_probability"])
#             print(detection["box_points"])
#             cv2.rectangle(frame, detection["box_points"][0:2], detection["box_points"][2:4], (0, 255, 0), 2)
#             cv2.putText(frame, detection["name"], (detection["box_points"][0], detection["box_points"][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

#         cv2.imshow("Frame", frame)
#     else:
#         print("Can't receive frame (stream end?). Exiting ...") 
#     key = cv2.waitKey(1)
#     if key == ord("q"):
#         break


    
# camera.release()
# cv2.destroyAllWindows()
import cv2
import numpy as np
import supervision as sv
from ultralytics import YOLO

model = YOLO("yolov8n.pt")
tracker = sv.ByteTrack()
box_annotator = sv.BoundingBoxAnnotator()
label_annotator = sv.LabelAnnotator()
trace_annotator = sv.TraceAnnotator()

def callback(frame: np.ndarray, _: int) -> np.ndarray:
    results = model(frame)[0]
    detections = sv.Detections.from_ultralytics(results)
    detections = tracker.update_with_detections(detections)

    labels = [
        f"#{tracker_id} {results.names[class_id]}"
        for class_id, tracker_id
        in zip(detections.class_id, detections.tracker_id)
    ]

    annotated_frame = box_annotator.annotate(
        frame.copy(), detections=detections)
    annotated_frame = label_annotator.annotate(
        annotated_frame, detections=detections, labels=labels)
    return trace_annotator.annotate(
        annotated_frame, detections=detections)

# sv.process_video(
#     source_path="people-walking.mp4",
#     target_path="result.mp4",
#     callback=callback
# )

# Open a camera for video capturing
camera = cv2.VideoCapture(0)  # 0 is usually the default camera

while True:
    ret, frame = camera.read()
    if not ret:
        print("Failed to grab frame")
        break

    processed_frame = callback(frame, 0)

    # Display the processed frame
    cv2.imshow('Processed Frame', processed_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
        break

camera.release()
cv2.destroyAllWindows()