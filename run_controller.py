from multiprocessing import Process
from threading import Thread

from controller.camera_server import receive_video_stream
from controller.controller_server import send_commands
from controller.keyboard_listener import run_keyboard_listener
from controller.variable_initialization import GlobalVariables

if __name__ == '__main__':
    global_variables = GlobalVariables()
    Process(target=receive_video_stream, args=(global_variables.shared_frame,)).start()
    Thread(target=run_keyboard_listener).start()
    send_commands()
