from controller.singleton import Singleton
from enums import MovementType, CommandKeys
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

    def forward(self) -> dict:
        """
        move car forward or backward, default value is forward

        """

        forward_command = {
            CommandKeys.COMMAND_TYPE: MovementType.FORWARD,
            CommandKeys.MOVE_SPEED: self.base_user_command[CommandKeys.MOVE_SPEED],
            CommandKeys.MOVE_DURATION: self.base_user_command[CommandKeys.MOVE_DURATION]
        }

        return forward_command

    def backward(self):

        backward_command = {
            CommandKeys.COMMAND_TYPE: MovementType.BACKWARD,
            CommandKeys.MOVE_SPEED: self.base_user_command[CommandKeys.MOVE_SPEED],
            CommandKeys.MOVE_DURATION: self.base_user_command[CommandKeys.MOVE_DURATION]
        }

        return backward_command

    def left(self):

        left_rotate_command = {
            CommandKeys.COMMAND_TYPE: MovementType.LEFT,
            CommandKeys.ROTATE_DURATION: CarSettings.ROTATE_DURATION,
            CommandKeys.ROTATE_SPEED: self.base_user_command[CommandKeys.ROTATE_SPEED],
        }

        return left_rotate_command

    def right(self):

        right_rotate_command = {
            CommandKeys.COMMAND_TYPE: MovementType.RIGHT,
            CommandKeys.ROTATE_DURATION: CarSettings.ROTATE_DURATION,
            CommandKeys.ROTATE_SPEED: self.base_user_command[CommandKeys.ROTATE_SPEED],
        }

        return right_rotate_command

    def stop(self):
        stop_command = {
            CommandKeys.COMMAND_TYPE: MovementType.STOP
        }

        return stop_command

    def build_commands(self, event_keys: list, *, stop_car: bool = False, autonomous: bool = False, frame=None) -> dict:

        if autonomous:
            assert frame
            pass

        if stop_car:
            command = self.stop()
            return command

        movement_types = set([movement_mapper.get(each_event_key) for each_event_key in event_keys])

        if MovementType.FORWARD in movement_types:
            command = self.forward()

        elif MovementType.BACKWARD in movement_types:
            command = self.backward()

        elif MovementType.RIGHT in movement_types:
            command = self.right()

        elif MovementType.LEFT in movement_types:
            command = self.left()
        else:
            command = {}

        return command
