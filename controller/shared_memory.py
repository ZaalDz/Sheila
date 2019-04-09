from threading import Lock
from controller.singleton import Singleton
from multiprocessing import Array
import ctypes
import numpy as np

shared_array = Array(ctypes.c_uint16, 720 * 480 * 3, lock=False)
shared_frame = np.frombuffer(shared_array, dtype=np.uint16)
shared_frame = shared_frame.reshape((480, 720, 3))


class SharedMemoryForCommands(metaclass=Singleton):

    def __init__(self):
        self.command_lock = Lock()
        self.valid_command_lock = Lock()

        self.command = None
        self._open = True

    def add_command(self, command_dict: dict):
        with self.command_lock:
            self.command = command_dict

    def get_command(self):
        with self.command_lock:
            if self.command:
                if self.is_open():
                    self.close()

                    command = self.command
                    self.command = None

                    return command
            return None

    def open(self):
        with self.valid_command_lock:
            self._open = True

    def close(self):
        with self.valid_command_lock:
            self._open = False

    def is_open(self):
        with self.valid_command_lock:
            return self._open
