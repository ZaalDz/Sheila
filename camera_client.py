import io
import socket
import struct
import time

import picamera

from settings import PORT, IP


def send_video_stream(connection):
    try:
        with picamera.PiCamera() as camera:
            camera.resolution = (640, 480)
            # Start a preview and let the camera warm up for 2 seconds
            camera.start_preview()

            time.sleep(2)

            # Note the start time and construct a stream to hold image data
            # temporarily (we could write it directly to connection but in this
            # case we want to find out the size of each capture first to keep
            # our protocol simple)

            stream = io.BytesIO()
            for _ in camera.capture_continuous(stream, 'jpeg'):
                # Write the length of the capture to the stream and flush to
                # ensure it actually gets sent
                connection.write(struct.pack('<L', stream.tell()))
                connection.flush()
                # Rewind the stream and send the image data over the wire
                stream.seek(0)
                connection.write(stream.read())
                # Reset the stream for the next capture
                stream.seek(0)
                stream.truncate()
        # Write a length of zero to the stream to signal we're done
        connection.write(struct.pack('<L', 0))
    finally:
        connection.close()

def connect_to_server(client_socket, ip, port):
    # Connect a client socket to my_server:8000 (change my_server to the
    # hostname of your server)
    client_socket.connect((IP, PORT))

    # Make a file-like object out of the connection
    connection = client_socket.makefile('wb')
    return connection


def main():
    while True:
        time.sleep(2)
        try:
            client_socket = socket.socket()
            print('Trying to start streaming')
            connection = connect_to_server(client_socket, IP, PORT)
            send_video_stream(connection)
        finally:
            client_socket.close()


if __name__ == '__main__':
    main()
