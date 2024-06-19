import cv2

url = 'http://192.168.41.95/1024x768.mjpeg'

cap = cv2.VideoCapture(url)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # If frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame', gray)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) == ord('q'):
        break

# When everything done, release the VideoCapture object
cap.release()

# Close all the frames
cv2.destroyAllWindows()