import socket
import time
from util import send_message, receive_message
from settings import CONTROLLER_PORT, IP


def start_dialog(conn):
    while True:
        recv = receive_message(conn)
        send_message(conn, recv)
        if not recv:
            print('Connection broke')
            break


def connect_to_server(my_socket: socket.socket):
    try:
        my_socket.connect((IP, CONTROLLER_PORT))
        print('Connection established')
        return True
    except socket.error as e:
        print(e)
        time.sleep(1)
        return False


def receive_commands():
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
            is_connected = connect_to_server(conn)
            if is_connected:
                start_dialog(conn)
