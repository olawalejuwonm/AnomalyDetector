import cv2
import numpy as np
import urllib.request

stream = urllib.request.urlopen('http://192.168.41.95/1024x768.mjpeg')

bytes = b''

while True:
    bytes += stream.read(1024)
    a = bytes.find(b'\xff\xd8')
    b = bytes.find(b'\xff\xd9')

    if a != -1 and b != -1:
        jpg = bytes[a:b+2]
        bytes = bytes[b+2:]
        img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
        # record the video and save to file
        # record the video and save to file
        # out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'MP4V'), 20.0, (640, 480))
        # out.write(img)
        # save the image
        cv2.imwrite('output.jpg', img)

        cv2.imshow('Video', img)

        if cv2.waitKey(1) == 27:  # Exit on ESC key
            exit(0)