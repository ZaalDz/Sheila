import socket
from json import dumps, loads


def send_command_dict(connection: socket.socket, command_dict: dict) -> None:

    command_to_string = dumps(command_dict)

    connection.send(command_to_string.encode())


def receive_command_dict(connection: socket.socket, buffer_size: int = 1024) -> dict:
    response = connection.recv(buffer_size)
    decoded_response = response.decode()
    return loads(decoded_response)
