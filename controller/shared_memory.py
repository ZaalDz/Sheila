from threading import Lock

from controller.gather_data import save_data
from controller.singleton import Singleton


class SharedMemoryForCommands(metaclass=Singleton):

    def __init__(self, shared_frame):
        self.command_lock = Lock()

        self.command = None
        self._open = True
        self.shared_frame = shared_frame

    def add_command(self, command_dict: dict):
        with self.command_lock:
            self.command = command_dict

    def get_command(self):
        with self.command_lock:
            if self.command:
                command = self.command
                self.command = None
                save_data(self.shared_frame, command)
                return command
            return None


