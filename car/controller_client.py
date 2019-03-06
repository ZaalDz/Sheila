from twisted.internet import reactor
from twisted.internet.protocol import ReconnectingClientFactory
from twisted.protocols.basic import LineReceiver

from settings import CONTROLLER_PORT, IP
from util import decode_command
from car.commander import run_command


class CommandReceiver(LineReceiver):
    def rawDataReceived(self, data):
        pass

    def connectionMade(self):
        self.setLineMode()

    def lineReceived(self, line):
        recv_command: dict = decode_command(line)

        run_command(recv_command)

        self.sendLine('Done'.encode())


class CommandClientFactory(ReconnectingClientFactory):
    protocol = CommandReceiver

    def __init__(self):
        super().__init__()
        self.maxDelay = 5

    def buildProtocol(self, addr):
        print('Connected.')
        self.resetDelay()
        return CommandReceiver()

    def clientConnectionLost(self, connector, reason):
        print('Lost connection.')
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        print('Connection failed.')
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)


def receive_commands():
    factory = CommandClientFactory()
    reactor.connectTCP(IP, CONTROLLER_PORT, factory)
    reactor.run()


if __name__ == '__main__':
    receive_commands()
