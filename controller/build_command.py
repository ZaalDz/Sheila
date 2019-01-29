from threading import Thread

from pynput.keyboard import Listener

from enums import MovementType, CommandKeys
from settings import MIN_CAMERA_POSITION, MIN_LEFT_TURN, MAX_CAMERA_POSITION, MAX_RIGHT_TURN

movement_mapper = {
    "'w'": MovementType.FORWARD,
    "'s'": MovementType.BACKWARD,
    "'a'": MovementType.LEFT,
    "'d'": MovementType.RIGHT,
    "'q'": MovementType.CAMERA_UP,
    "'z'": MovementType.CAMERA_DOWN
}

user_command = {
    CommandKeys.COMMAND_EXIST: False,
    CommandKeys.MOVEMENT_TYPE: None,
    CommandKeys.DURATION: 0.5,
    CommandKeys.SPEED: 50,
    CommandKeys.CAMERA_ROTATION_DEGREE: 7,
    CommandKeys.CAR_ROTATION_DEGREE: 10
}


def build_command():
    command_exist = user_command[CommandKeys.COMMAND_EXIST]
    movement_type = user_command[CommandKeys.MOVEMENT_TYPE]

    camera_degree = user_command[CommandKeys.CAMERA_ROTATION_DEGREE]
    car_rotation_degree = user_command[CommandKeys.CAR_ROTATION_DEGREE]

    if not command_exist:
        return {}

    if movement_type == MovementType.LEFT and car_rotation_degree > MIN_LEFT_TURN:
        user_command[CommandKeys.CAR_ROTATION_DEGREE] -= 1

    elif movement_type == MovementType.RIGHT and car_rotation_degree < MAX_RIGHT_TURN:
        user_command[CommandKeys.CAR_ROTATION_DEGREE] += 1

    elif movement_type == MovementType.CAMERA_DOWN and camera_degree > MIN_CAMERA_POSITION:
        user_command[CommandKeys.CAMERA_ROTATION_DEGREE] -= 1

    elif movement_type == MovementType.CAMERA_UP and camera_degree < MAX_CAMERA_POSITION:
        user_command[CommandKeys.CAMERA_ROTATION_DEGREE] += 1

    return user_command


def on_press(key):
    global user_command

    movement = movement_mapper.get(str(key))

    if movement:
        user_command[CommandKeys.MOVEMENT_TYPE] = movement
        user_command[CommandKeys.COMMAND_EXIST] = True

    else:
        user_command[CommandKeys.COMMAND_EXIST] = False


def on_release(key):
    global user_command
    print(f'{key} release')
    user_command[CommandKeys.COMMAND_EXIST] = False


def keyboard_listener():
    # Collect events until released
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


def run_keyboard_listener():
    Thread(target=keyboard_listener).start()
