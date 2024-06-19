import cv2
import os
from imageai.Detection import ObjectDetection
import numpy as np
import urllib.request

# camera = cv2.VideoCapture(0)
execution_path = os.getcwd()

detector = ObjectDetection()
detector.setModelTypeAsTinyYOLOv3()
detector.setModelPath(os.path.join(execution_path, "tiny-yolov3.pt"))

detector.loadModel()
stream = urllib.request.urlopen('http://192.168.41.95/1024x768.mjpeg')

bytes = b''

while True:

    # ret, frame = camera.read()

    bytes += stream.read(1024)
    a = bytes.find(b'\xff\xd8')
    b = bytes.find(b'\xff\xd9')

    if a != -1 and b != -1:
        jpg = bytes[a:b+2]
        bytes = bytes[b+2:]
        frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

        # Check if the frame is not empty
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


    
# camera.release()
cv2.destroyAllWindows()