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



def make_batch(offset: int, count: int):
    command = ffmpeg_command.generate_for_images(number_images[offset:offset+count], competitor_images[offset:offset+count], f"out/batches/out_{offset:010d}.mp4")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"Error occured. Exiting")
        exit()


def render_top_video():
    global number_images, competitor_images, top_length

    # number of simultaneously opened files will be twice as big
    max_batch_size = 200
    pictures_done = 0

    if top_length <= max_batch_size:
        command = ffmpeg_command.generate_for_images(number_images, competitor_images, f"out/top.mp4")
        subprocess.run(command, shell=True)
    else:
        os.makedirs("out/batches", exist_ok=True)

        while pictures_done < top_length:
            make_batch(pictures_done, max_batch_size)
            pictures_done += max_batch_size

        # batches = sorted(glob.glob("out/batches/*"))
        # merge_command = ffmpeg_command.generate_for_videos(batches, "out/top.mp4")
        # subprocess.run(merge_command, shell=True)


def compose_final_video(intro_file: str, outro_file: str, top_files: list, output_path: str):
    template = "ffmpeg {input} -f concat -safe 0 -i out/music-concat.txt -shortest -filter_complex \"{filter}\" -b:v 250k -b:a 55k -preset ultrafast '{output}'"
    videos = []
    videos.append(intro_file)
    videos.extend(top_files)
    videos.append(outro_file)
    input = ffmpeg_command.generate_video_input(videos)
    filter = ffmpeg_command.generate_filter_for_videos(videos, 1)
    command = template.format(input=input, filter=filter, output=output_path)
    print(command)
    subprocess.run(command, shell=True)


# FIXME: automate all the previous steps
# render_top_video()

compose_final_video("out/intro.mp4", "out/outro.mp4", sorted(glob.glob("out/batches/*")), "out/final.mp4")
