from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver

from controller.keyboard_listener import commands_list
from settings import CONTROLLER_PORT
from util import encode_command, decode_command


class Commander(LineReceiver):

    def rawDataReceived(self, data):
        pass

    def send_commands(self):

        command: list = commands_list.get_command()
        if command:
            encoded_command: bytes = encode_command(command)
            self.sendLine(encoded_command)

        reactor.callLater(0, self.send_commands)

    def connectionMade(self):
        print('Connection established')
        self.setLineMode()
        self.send_commands()

    def lineReceived(self, data):
        print(f'response: {decode_command(data)}')


def send_commands():
    factory = Factory()
    factory.protocol = Commander
    reactor.listenTCP(CONTROLLER_PORT, factory)
    reactor.run()
