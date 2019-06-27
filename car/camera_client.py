import subprocess
from subprocess import DEVNULL

from settings import VIDEO_SIZE, IP, STREAMING_PORT

streaming_command = f"""ffmpeg -f v4l2 -i /dev/video0 -threads 4 -s {VIDEO_SIZE} -c:v h264_omx -r 32 -f h264 udp://{IP}:{STREAMING_PORT}"""


def start_video_streaming():
    subprocess.call(streaming_command, shell=True, stderr=DEVNULL, stdout=DEVNULL)


if __name__ == '__main__':
    start_video_streaming()
