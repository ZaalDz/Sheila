from twisted.internet import reactor
from twisted.internet.protocol import ReconnectingClientFactory
from twisted.protocols.basic import LineReceiver

from settings import CONTROLLER_PORT, IP
from util import decode_command
from car.run_car_commands import commands_queue


class CommandReceiver(LineReceiver):
    def rawDataReceived(self, data):
        pass

    def connectionMade(self):
        self.setLineMode()

    def lineReceived(self, line):
        recv_command: dict = decode_command(line)
        print(f"**** {recv_command}")

        if commands_queue.qsize() == 0:
            commands_queue.put_nowait(recv_command)


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
