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


def receive_video_stream(shared_frame, driver, driver_color):
    cap = catch_open_stream()
    font = cv2.FONT_HERSHEY_SIMPLEX

    while True:
        ret, frame = cap.read()
        if not ret:
            print('frame empty')
            break
        shared_frame[:] = frame
        show_frame = frame.copy()

        height, width, _ = show_frame.shape
        start_x, start_y = int(width / 2 - 50), 10
        # cv2.putText(img=show_frame,
        #             text=driver,
        #             org=(start_x, start_y),
        #             fontFace=font,
        #             fontScale=1,
        #             color=driver_color,
        #             thickness=1)
        cv2.imshow('image', show_frame)

        if cv2.waitKey(1) & 0XFF == ord('p'):
            break

    cap.release()
    cv2.destroyAllWindows()
