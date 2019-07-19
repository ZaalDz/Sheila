from controller.singleton import Singleton
from enums import MovementType, CommandKeys, Driver
from settings import CarSettings

movement_mapper = {
    "'w'": MovementType.FORWARD,
    "'s'": MovementType.BACKWARD,
    "'a'": MovementType.LEFT,
    "'d'": MovementType.RIGHT,
}


class CommandBuilder(metaclass=Singleton):

    def __init__(self):

        self.base_user_command = {
            CommandKeys.MOVE_DURATION: CarSettings.MOVE_DURATION,
            CommandKeys.ROTATE_DURATION: CarSettings.ROTATE_DURATION,
            CommandKeys.MOVE_SPEED: CarSettings.CAR_SPEED,
            CommandKeys.ROTATE_SPEED: CarSettings.ROTATE_SPEED
        }

    @staticmethod
    def change_driver(command, autonomous_driver: bool = False):
        if autonomous_driver:
            command[CommandKeys.DRIVER] = Driver.AUTONOMOUS
        else:
            command[CommandKeys.DRIVER] = Driver.MANUAL

    def forward(self, autonomous_driver: bool = False) -> dict:
        """
        move car forward or backward, default value is forward

        """

        forward_command = {
            CommandKeys.COMMAND_TYPE: MovementType.FORWARD,
            CommandKeys.MOVE_SPEED: self.base_user_command[CommandKeys.MOVE_SPEED],
            CommandKeys.MOVE_DURATION: self.base_user_command[CommandKeys.MOVE_DURATION]
        }

        self.change_driver(forward_command, autonomous_driver)

        return forward_command

    def backward(self, autonomous_driver: bool = False):

        backward_command = {
            CommandKeys.COMMAND_TYPE: MovementType.BACKWARD,
            CommandKeys.MOVE_SPEED: self.base_user_command[CommandKeys.MOVE_SPEED],
            CommandKeys.MOVE_DURATION: self.base_user_command[CommandKeys.MOVE_DURATION]
        }

        self.change_driver(backward_command, autonomous_driver)

        return backward_command

    def left(self, autonomous_driver: bool = False):

        left_rotate_command = {
            CommandKeys.COMMAND_TYPE: MovementType.LEFT,
            CommandKeys.ROTATE_DURATION: CarSettings.ROTATE_DURATION,
            CommandKeys.ROTATE_SPEED: self.base_user_command[CommandKeys.ROTATE_SPEED],
        }

        self.change_driver(left_rotate_command, autonomous_driver)

        return left_rotate_command

    def right(self, autonomous_driver: bool = False):

        right_rotate_command = {
            CommandKeys.COMMAND_TYPE: MovementType.RIGHT,
            CommandKeys.ROTATE_DURATION: CarSettings.ROTATE_DURATION,
            CommandKeys.ROTATE_SPEED: self.base_user_command[CommandKeys.ROTATE_SPEED],
        }

        self.change_driver(right_rotate_command, autonomous_driver)

        return right_rotate_command

    def stop(self, autonomous_driver: bool = False):

        stop_command = {
            CommandKeys.COMMAND_TYPE: MovementType.STOP
        }

        self.change_driver(stop_command, autonomous_driver)

        return stop_command

    def build_commands(self, event_keys: list, *, stop_car: bool = False, autonomous: bool = False, frame=None) -> dict:

        movement_types = set(
            [movement_mapper.get(each_event_key) for each_event_key in event_keys])  # if not autonomous \
        #    else autonomous_driver(frame)
        # TODO implement actual autonomous driving function

        if stop_car:
            command = self.stop(autonomous_driver=autonomous)
            return command

        if MovementType.FORWARD in movement_types:
            command = self.forward(autonomous_driver=autonomous)

        elif MovementType.BACKWARD in movement_types:
            command = self.backward(autonomous_driver=autonomous)

        elif MovementType.RIGHT in movement_types:
            command = self.right(autonomous_driver=autonomous)

        elif MovementType.LEFT in movement_types:
            command = self.left(autonomous_driver=autonomous)
        else:
            command = {}

        return command
