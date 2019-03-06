from threading import Lock
from controller.singleton import Singleton


class SynchronizedList(list, metaclass=Singleton):

    def __init__(self):
        super().__init__()
        self.lock = Lock()
        self._open = True

    def add_command(self, command_dict: dict):
        with self.lock:
            # don't add command if it already added in list
            if not self or self[-1] != command_dict:
                self[0] = command_dict
                # super().append(command_dict)

    def get_command(self):
        """
        Returns: command dictionary or None if command list is empty

        """
        if self and self.is_open():
            self.close()
            return super().pop(0)

        return None

    def open(self):
        with self.lock:
            self._open = True

    def close(self):

        with self.lock:
            self._open = False

    def is_open(self):
        return self._open
