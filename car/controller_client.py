from twisted.internet import reactor
from twisted.internet.protocol import ReconnectingClientFactory
from twisted.protocols.basic import LineReceiver

from car.car import Car
from enums import CommandKeys, MovementType
from settings import CONTROLLER_PORT, IP
from util import decode_command

car = Car(pwm_frequency=150)


def run_command(receive_command: dict):
    movement_type = receive_command[CommandKeys.MOVEMENT_TYPE]
    speed = receive_command[CommandKeys.SPEED]
    move_duration = receive_command[CommandKeys.MOVE_DURATION]

    if movement_type in {MovementType.FORWARD, MovementType.BACKWARD}:
        car.move(speed, movement_type, move_duration)

    elif movement_type in {MovementType.FORWARD_RIGHT, MovementType.FORWARD_LEFT}:
        degree = receive_command[CommandKeys.CAR_ROTATION_DEGREE]
        car.forward_left_right(speed, degree, move_duration)

    elif movement_type in {MovementType.BACKWARD_RIGHT, MovementType.BACKWARD_LEFT}:
        degree = receive_command[CommandKeys.CAR_ROTATION_DEGREE]
        car.backward_left_right(speed, degree, move_duration)


class CommandReceiver(LineReceiver):
    def rawDataReceived(self, data):
        pass

    def connectionMade(self):
        self.setLineMode()

    def lineReceived(self, line):
        recv_command: dict = decode_command(line)
        print(f"received command: {recv_command}")
        run_command(recv_command)


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
