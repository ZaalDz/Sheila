import socket
import time

from car.car import Car, Directions
from settings import CONTROLLER_PORT, IP
from util import send_message, receive_message

car = Car(pwm_frequency=150)

movement_dict = {
    "'w'": Directions.FORWARD,
    "'s'": Directions.BACKWARD,
}


def start_controlling_car(conn):
    while True:
        recv = receive_message(conn)
        print(f"receive information: {recv}")
        move_direction = movement_dict.get(recv)
        print(f"move direction: {move_direction}")
        if move_direction:
            car.move(move_direction, 0.5, 50)

        send_message(conn, recv)
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
