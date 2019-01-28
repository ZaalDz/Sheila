import socket
from threading import Thread

from pynput.keyboard import Listener

from settings import CONTROLLER_PORT
from util import send_message, receive_message


def accepting_connection(my_socket: socket.socket) -> socket.socket:
    print('Trying to accept connection')
    connection, address = my_socket.accept()
    print('Connection established')
    return connection


def send_commands():
    user_input = ''

    def on_press(key):
        nonlocal user_input

        user_input = f'{key}'
        print(f'{key} pressed')

    def on_release(key):
        nonlocal user_input
        print(f'{key} release')
        user_input = ''

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
                if user_input:
                    send_message(conn, user_input)
                    response = receive_message(conn)
                    print(f'response from car: {response}')


