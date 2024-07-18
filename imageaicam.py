import cv2
import os
from imageai.Detection import ObjectDetection

camera = cv2.VideoCapture(0)
execution_path = os.getcwd()

detector = ObjectDetection()
detector.setModelTypeAsTinyYOLOv3()
detector.setModelPath(os.path.join(execution_path, "tiny-yolov3.pt"))
detector.loadModel()

# Create Background Subtractor
backSub = cv2.bgsegm.BackgroundSubtractorGSOC()
while True:
    ret, frame = camera.read()

    if ret:
        # Apply background subtraction
        fgMask = backSub.apply(frame)

        # Save the frame to a file
        # cv2.imwrite('output.jpg', frame)
        # detections = detector.detectObjectsFromImage(input_image='output.jpg')

        # for detection in detections:
        #     print(detection["name"], " : ", detection["percentage_probability"])
        #     print(detection["box_points"])
        #     cv2.rectangle(frame, detection["box_points"][0:2], detection["box_points"][2:4], (0, 255, 0), 2)
        #     cv2.putText(frame, detection["name"], (detection["box_points"][0], detection["box_points"][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # # Detect object contours
        # contours, _ = cv2.findContours(fgMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # # Draw contour over any detected moving object
        # for contour in contours:
        #     if cv2.contourArea(contour) > 10000:  # Adjust the minimum contour area as needed
        #         (x, y, w, h) = cv2.boundingRect(contour)
        #         cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display the original frame with detections
        cv2.imshow("Frame", frame)
        # Display the foreground mask
        # cv2.imshow("FG Mask", fgMask)
    else:
        print("Can't receive frame (stream end?). Exiting ...")
    key = cv2.waitKey(1)
    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()