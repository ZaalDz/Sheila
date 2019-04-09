import json
import os
from time import time

import cv2

from settings import COMMAND_DATA_PATH, FRAME_DATA_PATH, GATHER_DATA


def save_data(frame, command, *, image_dir=FRAME_DATA_PATH, command_dir=COMMAND_DATA_PATH, gather_data=GATHER_DATA):

    if gather_data is False:
        return

    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    if not os.path.exists(command_dir):
        os.makedirs(command_dir)

    name = str(time()).replace('.', '')
    image_name = os.path.join(image_dir, f'{name}.jpg')
    command_name = os.path.join(command_dir, f'{name}.json')

    cv2.imwrite(image_name, frame)

    with open(command_name, 'w') as fl:
        json.dump(command, fl)
