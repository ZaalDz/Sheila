from threading import Lock


class SynchronizedList(list):

    def __init__(self):
        super().__init__()
        self.lock = Lock()

    def append(self, command_dict):
        """
        adding copy command in list, function doesn't add duplicate command
        Args:
            command_dict: command dictionary

        """
        with self.lock:
            if not self or self[-1] != command_dict:
                super().append(command_dict.copy())

    def get_command(self):
        """
        Returns: command dictionary or None if command list is empty

        """
        return super().pop(0) if self else None
