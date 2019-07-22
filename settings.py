STREAMING_PORT = 8888
CONTROLLER_PORT = 5555
IP = '*'


class CarSettings:
    CAR_SPEED = 0.4
    ROTATE_SPEED = 0.3
    MOVE_DURATION = 0.2
    ROTATE_DURATION = 0.2


FRAME_WIDTH = 1280
FRAME_HEIGHT = 720
VIDEO_SIZE = f'{FRAME_WIDTH}x{FRAME_HEIGHT}'

FRAME_DATA_PATH = '/data/images'
COMMAND_DATA_PATH = '/data/command'
GATHER_DATA = True

COMMAND_TYPE_FOR_SAVING = set(['forward', 'backward', 'left', 'right'])

MODEL_PATH = 'weights/sheila_88.7_v_0_1.pth'
MODEL_INPUT_SIZE = 224

try:
    from custom_settings import *
except:
    pass

'''
sudo modprobe bcm2835-v4l2d
'''
