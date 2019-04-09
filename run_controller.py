from multiprocessing import Process
from threading import Thread

from controller.camera_server import receive_video_stream
from controller.controller_server import send_commands
from controller.keyboard_listener import run_keyboard_listener
from controller.shared_memory import shared_frame

if __name__ == '__main__':
    Process(target=receive_video_stream, args=(shared_frame, )).start()
    Thread(target=run_keyboard_listener).start()
    send_commands()
