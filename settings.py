STREAMING_PORT = 8888
CONTROLLER_PORT = 5555
IP = '*'

MIN_LEFT_TURN = 5
MAX_RIGHT_TURN = 9

MIN_CAMERA_POSITION = 9
MAX_CAMERA_POSITION = 12

STARTING_CAMERA_POSITION = 9
STARTING_ROTATION_POSITION = 7


VIDEO_SIZE = '1280x800'

try:
    from custom_settings import *
except:
    pass
