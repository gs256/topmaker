import ffmpeg_command
import glob
import subprocess
import os


numbers_wildcard = "out/numbers/*.*"
competitors_wildcard = "out/competitors/*.*"
number_images = sorted(glob.glob(numbers_wildcard), reverse=True)
competitor_images = sorted(glob.glob(competitors_wildcard), reverse=True)

assert(len(number_images) <= len(competitor_images))
top_length = len(number_images)

if len(competitor_images) > top_length:
    competitor_images = competitor_images[:top_length]

# number of simultaneously opened files will be twice as big
max_batch_size = 200
pictures_done = 0


def make_batch(offset: int, count: int):
    command = ffmpeg_command.generate_for_images(number_images[offset:offset+count], competitor_images[offset:offset+count], f"out/batches/out_{offset:010d}.mp4")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"Error occured. Exiting")
        exit()


# FIXME: automate all the previous steps

if top_length <= max_batch_size:
    command = ffmpeg_command.generate_for_images(number_images, competitor_images, f"out/top.mp4")
    subprocess.run(command, shell=True)
else:
    os.makedirs("out/batches", exist_ok=True)

    while pictures_done < top_length:
        make_batch(pictures_done, max_batch_size)
        pictures_done += max_batch_size

    batches = sorted(glob.glob("out/batches/*"))
    print(f"Found {len(batches)} batches")
    merge_command = ffmpeg_command.generate_for_videos(batches, "out/top.mp4")
    subprocess.run(merge_command, shell=True)
