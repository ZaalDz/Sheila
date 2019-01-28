import socket
from threading import Thread

from pynput.keyboard import Listener

from settings import CONTROLLER_PORT
from util import send_command_dict, receive_command_dict
from enums import Directions, CommandKeys


direction_mapper = {
    "'w'": Directions.FORWARD,
    "'s'": Directions.BACKWARD
}


def accepting_connection(my_socket: socket.socket) -> socket.socket:
    print('Trying to accept connection')
    connection, address = my_socket.accept()
    print('Connection established')
    return connection


def send_commands():
    user_command = {
        CommandKeys.DIRECTION: None,
        CommandKeys.DURATION: 0.5,
        CommandKeys.SPEED: 50
    }

    def on_press(key):
        nonlocal user_command

        user_command[CommandKeys.DIRECTION] = direction_mapper.get(str(key))
        print(f'{key} pressed')

    def on_release(key):
        nonlocal user_command
        print(f'{key} release')
        user_command[CommandKeys.DIRECTION] = None

    def run_listener():
        # Collect events until released
        with Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

    Thread(target=run_listener).start()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as my_socket:
        my_socket.bind(('0.0.0.0', CONTROLLER_PORT))
        my_socket.listen(0)
        connection = accepting_connection(my_socket)
        with connection as conn:
            while True:
                if user_command[CommandKeys.DIRECTION]:
                    send_command_dict(conn, user_command)
                    response = receive_command_dict(conn)
                    print(f'response from car: {response}')
