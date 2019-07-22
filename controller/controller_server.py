from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver

from settings import CONTROLLER_PORT
from threading import Lock

from util import encode_command, decode_command
from controller.global_variables import GlobalVariables

global_variables = GlobalVariables()
shared_memory = global_variables.shared_memory


class Commander(LineReceiver):
    def __init__(self):
        self._open = True
        self.valid_command_lock = Lock()

    def open(self):
        with self.valid_command_lock:
            self._open = True

    def close(self):
        with self.valid_command_lock:
            self._open = False

    def is_open(self):
        with self.valid_command_lock:
            return self._open

    def rawDataReceived(self, data):
        pass

    def send_commands(self):
        if global_variables.is_manual_driver() and self.is_open():
            command: dict = shared_memory.get_command()
        elif global_variables.is_autonomy_driver() and self.is_open():
            command = None
        else:
            command = None

        if command:
            self.close()
            encoded_command: bytes = encode_command(command)
            self.sendLine(encoded_command)

        reactor.callLater(0, self.send_commands)

    def connectionMade(self):
        print('Connection established')
        self.setLineMode()
        self.send_commands()

    def lineReceived(self, data):
        self.open()
        print(f'response: {decode_command(data)}')


def send_commands():
    factory = Factory()
    factory.protocol = Commander
    reactor.listenTCP(CONTROLLER_PORT, factory)
    reactor.run()
