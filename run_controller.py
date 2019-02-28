from controller.camera_server import receive_video_stream
from controller.controller_server import send_commands
from controller.keyboard_listener import run_keyboard_listener
from threading import Thread

if __name__ == '__main__':
    Thread(target=receive_video_stream).start()
    Thread(target=run_keyboard_listener).start()
    send_commands()
