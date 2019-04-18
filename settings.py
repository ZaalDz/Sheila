STREAMING_PORT = 8888
CONTROLLER_PORT = 5555
IP = '*'


class CarSettings:
    MIN_LEFT_TURN = 6.5
    MAX_RIGHT_TURN = 10.5

    MIN_CAMERA_POSITION = 9
    MAX_CAMERA_POSITION = 13

    STARTING_CAMERA_POSITION = 13
    STARTING_ROTATION_POSITION = 8.5

    CAR_SPEED = 50
    MOVE_DURATION = 0.4
    ROTATE_DURATION = 0.4

    WHEEL_ROTATE_SPEED = 1
    CAMERA_ROTATE_SPEED = 1.5


VIDEO_SIZE = '720x480'

FRAME_DATA_PATH = '/data/images'
COMMAND_DATA_PATH = '/data/command'
GATHER_DATA = False

try:
    from custom_settings import *
except:
    pass

'''
sudo modprobe bcm2835-v4l2d
'''
