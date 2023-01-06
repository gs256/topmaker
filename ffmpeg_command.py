import config
import subprocess

transition_duration = 1

def generate_for_images(number_images: list, competitor_images: list, out_file: str) -> str:
    number_duration = 2
    competitor_duration = 3
    template = "ffmpeg {input} -c:v libx264 -filter_complex_script {filter} -pix_fmt yuvj422p -framerate 20 -preset ultrafast {out_file}"
    assert(len(number_images) > 0)
    assert(len(competitor_images) > 0)
    input_count = len(number_images) * 2
    input = generate_image_input(number_images, competitor_images, number_duration, competitor_duration, transition_duration)
    filter = generate_filter_for_images(input_count, config.WIDTH, config.HEIGHT, transition_duration, number_duration, competitor_duration)
    command = template.format(input=input, filter=filter, out_file=out_file)
    return command


def generate_for_videos(videos: list, out_file: str) -> str:
    template = "ffmpeg {input} -filter_complex \"{filter}\" -preset ultrafast {out_file}"
    assert(len(videos) > 0)
    input = generate_video_input(videos)
    filter = generate_filter_for_videos(videos, transition_duration)
    command = template.format(input=input, filter=filter, out_file=out_file)
    return command


def generate_video_input(videos: list) -> str:
    result = ""

    for video in videos:
        result += f" -i {video} "

    return result


def generate_image_input(number_images: list, competitor_images: list, number_duration: int, competitor_duration: int, transition_duration: int) -> str:
    assert(len(number_images) <= len(competitor_images))
    result = ""

    # FIXME: last one is longer due to the transition calculation
    for i in range(len(number_images)):
        result += f" -loop 1 -t {number_duration+transition_duration} -i {number_images[i]} "
        result += f" -loop 1 -t {competitor_duration+transition_duration} -i {competitor_images[i]} "

    return result


def generate_filter_for_videos(videos: list, transition_duration: int) -> str:
    template = "[{input1}][{input2}]xfade=radial:duration={duration}:offset={offset}"
    result = ""

    def calculate_offset(videos: list, index: int, transition_duration: int) -> int:
        result = 0
        for i in range(index+1):
            result += get_video_duration(videos[i])
        result -= transition_duration
        return result

    for i in range(len(videos)-1):
        offset = calculate_offset(videos, i, transition_duration)
        input1 = f"{i}:v" if i == 0 else f"v{i}o"
        addition = template.format(input1=input1, input2=f"{i+1}:v", duration=transition_duration, offset=offset)
        if i < len(videos) - 2:
            addition += "[v{next}o];".format(next=i+1)
        result += addition

    return result


def get_video_duration(path: str) -> int:
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)

    return int(float(result.stdout.decode()))


def generate_filter_for_images(input_count: int, width: int, height: int, transition_duration: int, number_duration: int, competitor_duration: int) -> str:
    input_config_template = "[{index}:v]scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,setsar=1[v{index}];"
    transition_template = "[{input1}][{input2}]xfade=transition=radial:duration={duration}:offset={offset}"
    transition_output_template = "[v{next}o];"
    result = ""

    for i in range(input_count):
        result += input_config_template.format(index=i, width=width, height=height)

    # number of transitions is less by one
    for i in range(input_count-1):
        offset = (number_duration+competitor_duration)*((i+1)//2) + number_duration*((i+1)%2)
        input1 = f"v{i}" if i == 0 else f"v{i}o"
        addition = transition_template.format(input1=input1, input2=f"v{i+1}", duration=transition_duration, offset=offset)
        if i < input_count - 2:
            addition += transition_output_template.format(next=i+1)
        result += addition

    out_path = "out/filter_complex_script.txt"
    with open(out_path, "w+") as file:
        file.write(result)

    return out_path


# result = generate()
# print(result)
