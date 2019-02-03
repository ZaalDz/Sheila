from threading import Lock
from controller.singleton import Singleton


class SynchronizedList(list, metaclass=Singleton):

    def __init__(self):
        super().__init__()
        self.lock = Lock()

    def add_command(self, command_list):
        with self.lock:

            # don't add command if it already added in list
            if not self or self[-1] != command_list:
                super().append(command_list)

    def get_command(self):
        """
        Returns: command dictionary or None if command list is empty

        """
        return super().pop(0) if self else None
