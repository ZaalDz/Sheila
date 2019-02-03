from threading import Thread
from pynput.keyboard import Listener
from controller.synchronized_list import SynchronizedList
from controller.build_command import CommandBuilder, movement_mapper

commands_list = SynchronizedList()
command_builder = CommandBuilder()

expected_keys = set(movement_mapper.keys())

pressed_keys = set()


def is_pressed_keys_valid(pressed_keys_set, expected_keys_set):
    return not pressed_keys_set - expected_keys_set


def on_press(event):

    key = str(event)
    pressed_keys.add(key)

    if is_pressed_keys_valid(pressed_keys, expected_keys):
        command = command_builder.build_commands(list(pressed_keys))
        commands_list.add_command(command)


def on_release(event):

    key = str(event)
    pressed_keys.remove(key)

    if is_pressed_keys_valid(pressed_keys, expected_keys) and key in {"'a'", "'d'"}:
        command = command_builder.build_commands(event_keys=[], set_wheel_default_position=True)
        commands_list.add_command(command)


def keyboard_listener():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


def run_keyboard_listener():
    Thread(target=keyboard_listener).start()
