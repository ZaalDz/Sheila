from car.camera_client import main
from threading import Thread

if __name__ == '__main__':
    Thread(target=main).start()
