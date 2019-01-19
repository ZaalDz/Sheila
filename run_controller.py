from controller.camera_server import receive_video_stream
from threading import Thread

if __name__ == '__main__':
    Thread(target=receive_video_stream).start()
