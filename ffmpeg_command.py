import glob


def generate_command() -> str:
    number_duration = 2
    competitor_duration = 3
    transition_duration = 1
    template = "ffmpeg {input} -c:v libx264 -filter_complex \"{filter}\" -pix_fmt yuvj422p -framerate 24 out.mp4"
    numbers_wildcard = "testnum/*.*"
    competitors_wildcard = "testcomp/*.*"
    number_images = sorted(glob.glob(numbers_wildcard), reverse=True)
    competitor_images = sorted(glob.glob(competitors_wildcard), reverse=True)
    input = generate_ffmpeg_input(number_images, competitor_images, number_duration, competitor_duration, transition_duration)
    filter = generate_complex_filter(len(number_images)+len(competitor_images), 854, 480, transition_duration, number_duration, competitor_duration)
    command = template.format(input=input, filter=filter)
    return command


def generate_ffmpeg_input(number_images: list, competitor_images: list, number_duration: int, competitor_duration: int, transition_duration: int) -> str:
    assert(len(number_images) == len(competitor_images))
    result = ""

    # FIXME: last one is longer due to the transition calculation
    for i in range(len(number_images)):
        result += f" -loop 1 -t {number_duration+transition_duration} -i {number_images[i]} "
        result += f" -loop 1 -t {competitor_duration+transition_duration} -i {competitor_images[i]} "

    return result


def generate_complex_filter(input_count: int, width: int, height: int, transition_duration: int, number_duration: int, competitor_duration: int) -> str:
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

    return result


result = generate_command()
print(result)