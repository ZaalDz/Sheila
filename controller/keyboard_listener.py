from pynput.keyboard import Listener

from controller.build_command import CommandBuilder, movement_mapper
from controller.shared_memory import SharedMemoryForCommands

shared_memory = SharedMemoryForCommands()
command_builder = CommandBuilder()

expected_keys = set(movement_mapper.keys())

pressed_keys = set()


def is_not_valid_move(key):
    return key == "'a'" and "'d'" in pressed_keys or \
           key == "'d'" and "'a'" in pressed_keys or \
           key == "'w'" and "'s'" in pressed_keys or \
           key == "'s'" and "'w'" in pressed_keys or \
           key == "'q'" and "'z'" in pressed_keys or \
           key == "'z'" and "'q'" in pressed_keys


def is_pressed_keys_valid(pressed_keys_set, expected_keys_set):
    return not pressed_keys_set - expected_keys_set


def on_press(event):
    key = str(event)
    pressed_keys.add(key)
    if is_not_valid_move(key):
        pressed_keys.remove(key)

    if is_pressed_keys_valid(pressed_keys, expected_keys):
        command = command_builder.build_commands(list(pressed_keys))
        if command:
            shared_memory.add_command(command)


def on_release(event):
    key = str(event)

    try:
        pressed_keys.remove(key)
    except:
        pass


def run_keyboard_listener():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
