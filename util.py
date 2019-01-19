import socket


def send_message(connection: socket.socket, message: str) -> None:
    connection.send(message.encode())


def receive_message(connection: socket.socket, buffer_size: int = 1024) -> str:
    response = connection.recv(buffer_size)
    return response.decode()
