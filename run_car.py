from car.camera_client import start_video_streaming
from car.controller_client import receive_commands
from car.run_car_commands import run_command
from threading import Thread

if __name__ == '__main__':
    Thread(target=start_video_streaming).start()
    Thread(target=run_command).start()
    receive_commands()
