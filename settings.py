STREAMING_PORT = 8888
CONTROLLER_PORT = 5555
IP = '*'


class CarSettings:
    CAR_SPEED = 0.4
    ROTATE_SPEED = 0.3
    MOVE_DURATION = 0.2
    ROTATE_DURATION = 0.2


VIDEO_SIZE = '720x480'

FRAME_DATA_PATH = '/data/images'
COMMAND_DATA_PATH = '/data/command'
GATHER_DATA = False

COMMAND_TYPE_FOR_SAVING = set(['forward', 'backward', 'left', 'right'])

try:
    from custom_settings import *
except:
    pass

'''
sudo modprobe bcm2835-v4l2d
'''
