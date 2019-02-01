from threading import Thread, Lock
from controller.synchronized_list import SynchronizedList
from pynput.keyboard import Listener

from enums import MovementType, CommandKeys
from settings import MIN_CAMERA_POSITION, MIN_LEFT_TURN, MAX_CAMERA_POSITION, MAX_RIGHT_TURN, \
    STARTING_CAMERA_POSITION, STARTING_ROTATION_POSITION, MOVE_DURATION, ROTATE_DURATION, CAR_SPEED

command_list = SynchronizedList()

movement_mapper = {
    "'w'": MovementType.FORWARD,
    "'s'": MovementType.BACKWARD,
    "'a'": MovementType.LEFT,
    "'d'": MovementType.RIGHT,
    "'q'": MovementType.CAMERA_UP,
    "'z'": MovementType.CAMERA_DOWN
}

user_command = {
    CommandKeys.MOVEMENT_TYPE: None,
    CommandKeys.MOVE_DURATION: MOVE_DURATION,
    CommandKeys.ROTATE_DURATION: ROTATE_DURATION,
    CommandKeys.SPEED: CAR_SPEED,
    CommandKeys.CAMERA_ROTATION_DEGREE: STARTING_CAMERA_POSITION,
    CommandKeys.CAR_ROTATION_DEGREE: STARTING_ROTATION_POSITION
}


def set_movement_type(key, change_car_to_default_position=False):
    global user_command

    movement = movement_mapper.get(str(key))

    if movement:
        user_command[CommandKeys.MOVEMENT_TYPE] = movement
        CommandBuilder.build_command(change_car_to_default_position)


class CommandBuilder:
    lock = Lock()

    @staticmethod
    def build_command(change_car_to_default_position):

        if not change_car_to_default_position:
            movement_type = user_command[CommandKeys.MOVEMENT_TYPE]

            camera_degree = user_command[CommandKeys.CAMERA_ROTATION_DEGREE]
            car_rotation_degree = user_command[CommandKeys.CAR_ROTATION_DEGREE]

            if movement_type == MovementType.LEFT and car_rotation_degree > MIN_LEFT_TURN:
                user_command[CommandKeys.CAR_ROTATION_DEGREE] -= 1

            elif movement_type == MovementType.RIGHT and car_rotation_degree < MAX_RIGHT_TURN:
                user_command[CommandKeys.CAR_ROTATION_DEGREE] += 1

            elif movement_type == MovementType.CAMERA_DOWN and camera_degree > MIN_CAMERA_POSITION:
                user_command[CommandKeys.CAMERA_ROTATION_DEGREE] -= 1

            elif movement_type == MovementType.CAMERA_UP and camera_degree < MAX_CAMERA_POSITION:
                user_command[CommandKeys.CAMERA_ROTATION_DEGREE] += 1

        command_list.append(user_command)

    @staticmethod
    def on_press(key):
        with CommandBuilder.lock:
            set_movement_type(key)

    @staticmethod
    def on_release(key):
        with CommandBuilder.lock:
            global user_command

            if str(key) in {"'a'", "'d'"}:
                user_command[CommandKeys.CAR_ROTATION_DEGREE] = STARTING_ROTATION_POSITION
                set_movement_type(key, change_car_to_default_position=True)


def keyboard_listener():
    # Collect events until released
    with Listener(on_press=CommandBuilder.on_press, on_release=CommandBuilder.on_release) as listener:
        listener.join()


def run_keyboard_listener():
    Thread(target=keyboard_listener).start()
