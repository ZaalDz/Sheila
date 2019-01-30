import subprocess
from subprocess import DEVNULL
from settings import VIDEO_SIZE, IP, STREAMING_PORT

streaming_command = f"""ffmpeg -f v4l2 -i /dev/video0 -preset ultrafast -s {VIDEO_SIZE} -vcodec libx264 -tune zerolatency -b 900k -f h264 udp://{IP}:{STREAMING_PORT}"""


def start_video_streaming():
    subprocess.call(streaming_command, shell=True, stderr=DEVNULL, stdout=DEVNULL)
