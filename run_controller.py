from controller.camera_server import receive_video_stream
from controller.controller_server import send_commands
from threading import Thread

if __name__ == '__main__':
    Thread(target=receive_video_stream).start()
    Thread(target=send_commands).start()
