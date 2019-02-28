from json import dumps, loads


def encode_command(command_dict: list) -> bytes:
    command_to_string = dumps(command_dict)

    return command_to_string.encode()


def decode_command(command_dict: bytes) -> list:
    decoded_command = command_dict.decode()
    return loads(decoded_command)
