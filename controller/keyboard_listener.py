from pynput.keyboard import Listener
from controller.global_variables import GlobalVariables

global_variable = GlobalVariables()


def is_not_valid_move(key, pressed_keys):
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
    if key == "'c'":
        global_variable.change_driver()

    if global_variable.is_manual_driver():
        global_variable.pressed_keys.add(key)
        if is_not_valid_move(global_variable.pressed_keys, key):
            global_variable.pressed_keys.remove(key)

        if is_pressed_keys_valid(global_variable.pressed_keys, global_variable.expected_keys):
            command = global_variable.command_builder.build_commands(list(global_variable.pressed_keys))
            if command:
                global_variable.shared_memory.add_command(command)


def on_release(event):

    key = str(event)
    if global_variable.is_manual_driver():
        try:
            global_variable.pressed_keys.remove(key)
            for each in global_variable.possible_movements:
                if each in global_variable.pressed_keys:
                    return
            command = global_variable.command_builder.build_commands([], stop_car=True)
            global_variable.shared_memory.add_command(command)
        except:
            pass


def run_keyboard_listener():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
