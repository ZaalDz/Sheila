import time

import cv2

from settings import STREAMING_PORT, IP


def catch_open_stream():
    while True:
        cap = cv2.VideoCapture(f'udp://{IP}:{STREAMING_PORT}')
        if cap.isOpened():
            return cap
        print("Trying to connect video streaming")
        time.sleep(3)


def receive_video_stream(shared_frame):
    cap = catch_open_stream()

    while True:
        ret, frame = cap.read()

        if not ret:
            print('frame empty')
            break
        shared_frame[:] = frame
        cv2.imshow('image', frame)

        if cv2.waitKey(1) & 0XFF == ord('p'):
            break

    cap.release()
    cv2.destroyAllWindows()
