import ctypes
from multiprocessing import Array

import numpy as np

from controller.build_command import CommandBuilder, movement_mapper
from controller.shared_memory import SharedMemoryForCommands
from controller.singleton import Singleton


class GlobalVariables(metaclass=Singleton):
    def __init__(self):
        shared_array = Array(ctypes.c_uint16, 720 * 480 * 3, lock=False)
        shared_frame = np.frombuffer(shared_array, dtype=np.uint16)

        self.shared_frame = shared_frame.reshape((480, 720, 3))

        self.shared_memory = SharedMemoryForCommands(self.shared_frame)
        self.command_builder = CommandBuilder()

        self.expected_keys = set(movement_mapper.keys())
        self.pressed_keys = set()
        self.possible_movements = set(list(movement_mapper.keys()))

        self.autonomous_mode = False
