STREAMING_PORT = 8888
CONTROLLER_PORT = 5555
IP = '*'


class CarSettings:
    MIN_LEFT_TURN = 6.5
    MAX_RIGHT_TURN = 8.5

    MIN_CAMERA_POSITION = 9
    MAX_CAMERA_POSITION = 12

    STARTING_CAMERA_POSITION = 12
    STARTING_ROTATION_POSITION = 7.5

    CAR_SPEED = 50
    MOVE_DURATION = 0.4
    ROTATE_DURATION = 0.4

    WHEEL_ROTATE_SPEED = 1
    CAMERA_ROTATE_SPEED = 1


VIDEO_SIZE = '720x480'

try:
    from custom_settings import *
except:
    pass

'''
sudo modprobe bcm2835-v4l2d
'''
