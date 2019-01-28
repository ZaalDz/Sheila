import socket
import time

from car.car import Car
from settings import CONTROLLER_PORT, IP
from util import send_command_dict, receive_command_dict
from enums import CommandKeys

car = Car(pwm_frequency=150)


def start_controlling_car(conn):
    while True:
        recv = receive_command_dict(conn)
        if recv[CommandKeys.DIRECTION]:
            direction, speed, duration = recv[CommandKeys.DIRECTION], recv[CommandKeys.SPEED], recv[
                CommandKeys.DURATION]
            car.move(direction, duration, speed)

        send_command_dict(conn, recv)
        if not recv:
            print('Connection broke')
            break


def connect_to_server(my_socket: socket.socket):
    try:
        print('Trying to connect to controller')
        my_socket.connect((IP, CONTROLLER_PORT))
        print('Connection established')
        return True
    except socket.error as e:
        print(e)
        time.sleep(3)
        return False


def receive_commands():
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
            is_connected = connect_to_server(conn)
            if is_connected:
                start_controlling_car(conn)
