from multiprocessing import Process

from car.camera_client import start_video_streaming
from car.controller_client import receive_commands

if __name__ == '__main__':
    Process(target=start_video_streaming).start()
    receive_commands()
