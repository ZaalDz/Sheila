import asyncio

from twisted.internet import reactor
from twisted.internet.protocol import ReconnectingClientFactory
from twisted.protocols.basic import LineReceiver

from car.car import Car
from enums import CommandKeys, MovementType
from settings import CONTROLLER_PORT, IP
from util import decode_command, encode_command

car = Car(pwm_frequency=150)


async def create_async_tasks(recv_command_list):
    async_tasks = []

    for each_command in recv_command_list:

        movement_type = each_command[CommandKeys.MOVEMENT_TYPE]

        if movement_type in {MovementType.FORWARD, MovementType.BACKWARD}:
            speed = each_command[CommandKeys.SPEED]
            move_duration = each_command[CommandKeys.MOVE_DURATION]
            task = asyncio.create_task(car.move(speed=speed, direction=movement_type, duration=move_duration))

        elif movement_type in {MovementType.LEFT, MovementType.RIGHT, MovementType.DEFAULT_WHEEL_POSITION}:
            degree = each_command[CommandKeys.CAR_ROTATION_DEGREE]
            rotate_duration = each_command[CommandKeys.ROTATE_DURATION]
            task = asyncio.create_task(car.turn_lr(degree=degree, duration=rotate_duration))

        elif movement_type in {MovementType.CAMERA_UP, MovementType.CAMERA_DOWN,
                               MovementType.DEFAULT_CAMERA_POSITION}:

            degree = each_command[CommandKeys.CAMERA_ROTATION_DEGREE]
            rotate_duration = each_command[CommandKeys.ROTATE_DURATION]
            task = asyncio.create_task(car.camera_position(degree, duration=rotate_duration))
        # TODO: else?
        async_tasks.append(task)

    return await asyncio.gather(*async_tasks)


class CommandReceiver(LineReceiver):
    def rawDataReceived(self, data):
        pass

    def connectionMade(self):
        self.setLineMode()

    def lineReceived(self, line):
        recv_command: list = decode_command(line)
        response = asyncio.run(create_async_tasks(recv_command))
        feedback = encode_command(response)
        self.sendLine(feedback)


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
