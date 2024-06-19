import cv2
import os
from imageai.Detection import ObjectDetection

camera = cv2.VideoCapture(0)
execution_path = os.getcwd()

detector = ObjectDetection()
detector.setModelTypeAsTinyYOLOv3()
detector.setModelPath(os.path.join(execution_path, "tiny-yolov3.pt"))
detector.loadModel()

while True:

    ret, frame = camera.read()

    

    # Check if the frame is not empty
    if ret:
        # Save the frame to a file
        cv2.imwrite('output.jpg', frame)
        detections = detector.detectObjectsFromImage(input_image='output.jpg')

        for detection in detections:
            print(detection["name"], " : ", detection["percentage_probability"])
            print(detection["box_points"])
            cv2.rectangle(frame, detection["box_points"][0:2], detection["box_points"][2:4], (0, 255, 0), 2)
            cv2.putText(frame, detection["name"], (detection["box_points"][0], detection["box_points"][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow("Frame", frame)
    else:
        print("Can't receive frame (stream end?). Exiting ...") 
    key = cv2.waitKey(1)
    if key == ord("q"):
        break


    
camera.release()
cv2.destroyAllWindows()