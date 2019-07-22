import json
from pathlib import Path
from time import time

import cv2

from enums import CommandKeys
from settings import COMMAND_DATA_PATH, FRAME_DATA_PATH, GATHER_DATA, COMMAND_TYPE_FOR_SAVING


def save_data(frame, command, *, image_data_dir=FRAME_DATA_PATH, command_data_dir=COMMAND_DATA_PATH,
              gather_data=GATHER_DATA):
    image_data_dir = Path(image_data_dir)
    command_data_dir = Path(command_data_dir)
    if gather_data is False:
        return

    image_data_dir.mkdir(exist_ok=True)
    command_data_dir.mkdir(exist_ok=True)

    command_type = command[CommandKeys.COMMAND_TYPE]

    if command_type in COMMAND_TYPE_FOR_SAVING:
        final_image_data_path = image_data_dir / command_type
        final_command_data_path = command_data_dir / command_type

        final_image_data_path.mkdir(exist_ok=True)
        final_command_data_path.mkdir(exist_ok=True)

        name = f"{command_type}_{str(time()).replace('.', '')}"
        image_name = final_image_data_path / f'{name}.jpg'
        command_name = final_command_data_path / f'{name}.json'

        cv2.imwrite(str(image_name.absolute()), frame)

        with open(str(command_name.absolute()), 'w') as fl:
            json.dump(command, fl)
