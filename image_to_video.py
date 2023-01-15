import sys
import subprocess
import config

template = "ffmpeg {input} -c:v libx264 -filter_complex \"[0:v]scale={width}:{width}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,setsar=1\" -pix_fmt yuvj422p -framerate 20 -preset ultrafast '{out_file}'"


if len(sys.argv) < 3:
    print("Usage: image_to_video.py [PATH_TO_IMAGE] [DURATION_IN_SECONDS]")

path = sys.argv[1]
duration = sys.argv[2]

width = config.WIDTH
height = config.HEIGHT

input = f"-loop 1 -t {duration} -i '{path}'"
command = template.format(input=input, width=width, height=height, out_file=f"{path}.mp4")
print(command)
subprocess.run(command, shell=True)
