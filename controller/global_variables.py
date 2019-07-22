import ctypes
from multiprocessing import Array

import numpy as np

from controller.build_command import CommandBuilder, movement_mapper
from controller.shared_memory import SharedMemoryForCommands
from controller.singleton import Singleton
from settings import FRAME_HEIGHT, FRAME_WIDTH
from enums import Driver


class GlobalVariables(metaclass=Singleton):
    def __init__(self):
        shared_array = Array(ctypes.c_uint16, FRAME_HEIGHT * FRAME_WIDTH * 3, lock=False)
        shared_frame = np.frombuffer(shared_array, dtype=np.uint16)

        self.shared_frame = shared_frame.reshape((FRAME_HEIGHT, FRAME_WIDTH, 3))

        self.shared_memory = SharedMemoryForCommands(self.shared_frame)
        self.command_builder = CommandBuilder()
        self.driver = Driver.MANUAL
        self._red = (0, 255, 0)
        self._green = (0, 0, 255)
        self.driver_color = self._green

        self.expected_keys = set(movement_mapper.keys())
        self.pressed_keys = set()
        self.possible_movements = set(list(movement_mapper.keys()))

        self.autonomous_mode = False

    def change_driver(self):
        if self.driver == Driver.MANUAL:
            self.driver = Driver.AUTONOMOUS
            self.driver_color = self._green
        else:
            self.driver = Driver.MANUAL
            self.driver_color = self._red

    def is_manual_driver(self):
        return self.driver == Driver.MANUAL

    def is_autonomy_driver(self):
        return self.driver == Driver.AUTONOMOUS
