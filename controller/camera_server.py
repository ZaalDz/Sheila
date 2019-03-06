import time
import cv2
from settings import STREAMING_PORT, IP


def catch_open_stream():
    while True:
        cap = cv2.VideoCapture(f'udp://{IP}:{STREAMING_PORT}', cv2.CAP_FFMPEG)
        if cap.isOpened():
            return cap
        print("Trying to connect video streaming")
        time.sleep(2)


def receive_video_stream():
    cap = catch_open_stream()

    while True:
        ret, frame = cap.read()

        if not ret:
            print('frame empty')
            break

        cv2.imshow('image', frame)

        if cv2.waitKey(1) & 0XFF == ord('p'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    receive_video_stream()
