import socket

from settings import CONTROLLER_PORT
from util import send_command_dict, receive_command_dict
from controller.keyboard_listener import run_keyboard_listener
from controller.keyboard_listener import commands_list


def accepting_connection(my_socket: socket.socket) -> socket.socket:
    print('Trying to accept connection')
    connection, address = my_socket.accept()
    print('Connection established')
    return connection


def send_commands():

    run_keyboard_listener()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as my_socket:
        my_socket.bind(('0.0.0.0', CONTROLLER_PORT))
        my_socket.listen(0)
        connection = accepting_connection(my_socket)
        with connection as conn:
            while True:
                command = commands_list.get_command()
                if command:
                    send_command_dict(conn, command)
                    response = receive_command_dict(conn)
                    print(f'response from car: {response}')
