import glob
import subprocess
import os
import ffmpeg_command
import number_image_renderer
import image_query
import image_downloader
import music_concat


def make_batch(number_images: list, competitor_images: list, offset: int, count: int):
    command = ffmpeg_command.generate_for_images(number_images[offset:offset+count], competitor_images[offset:offset+count], f"out/batches/out_{offset:010d}.mp4")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"Error occured. Exiting")
        exit()


def compose_final_video(output_path: str):
    template = "ffmpeg {input} -f concat -safe 0 -i out/music-concat.txt -shortest -filter_complex \"{filter}\" -b:v 250k -b:a 55k -preset ultrafast '{output}'"
    videos = []
    intro_file = "out/intro.mp4"
    outro_file = "out/outro.mp4"
    top_files = sorted(glob.glob("out/batches/*"))
    videos.append(intro_file)
    videos.extend(top_files)
    videos.append(outro_file)
    input = ffmpeg_command.generate_video_input(videos)
    filter = ffmpeg_command.generate_filter_for_videos(videos, 1)
    command = template.format(input=input, filter=filter, output=output_path)
    print(command)
    subprocess.run(command, shell=True)


def choise_positive(choise: str) -> bool:
    if len(choise) == 0 or choise.lower()[0] != "y":
        return False
    return True


def offer_directory_cleanup(dir_path: str):
    files = glob.glob(dir_path+"*")
    if len(files) > 0:
        choise = input(f"The directory '{dir_path}' already has {len(files)} file(s). Remove? [Y/n]: ")
        if choise_positive(choise):
            [os.remove(p) for p in files]
        else:
            return


def render_number_images():
    offer_directory_cleanup("out/numbers/")
    print("Pictures will be saved to out/numbers/")
    count = int(input("Enter the number of pictures: "))
    number_image_renderer.render(count)


def get_image_urls():
    print("Json file with picture urls will be saved to out/image-query.json")
    query = input("Query: ")
    count = int(input("Number of pictures: "))
    image_query.query(query, count)


def download_images():
    offer_directory_cleanup("out/competitors/")

    if not os.path.exists("out/image-query.json"):
        print("Query file out/image-query.json is not found")
        return

    print("Images will be saved to out/competitors/")
    count = int(input("Number of images (0 means all): "))
    image_downloader.download(count)


def render_top():
    offer_directory_cleanup("out/batches/")

    numbers_wildcard = "out/numbers/*"
    competitors_wildcard = "out/competitors/*"
    number_images = sorted(glob.glob(numbers_wildcard), reverse=True)
    competitor_images = sorted(glob.glob(competitors_wildcard), reverse=True)

    print(f"Number images - {len(number_images)}")
    print(f"Competitor images - {len(competitor_images)}")

    if len(number_images) > len(competitor_images):
        print("Number of number images should be <= number of competitors")
        return

    if len(number_images) == 0 or len(competitor_images) == 0:
        print("Number of images should be > 0")
        return

    top_length = len(number_images)
    choise = input(f"The length of the top is {top_length}, correct? [Y/n]: ")

    if not choise_positive(choise):
        print("Check the amount of number images")
        return

    if len(competitor_images) > top_length:
        competitor_images = competitor_images[len(competitor_images)-top_length:]

    # number of simultaneously opened files will be twice as big
    max_batch_size = 200
    pictures_done = 0

    os.makedirs("out/batches", exist_ok=True)

    if top_length <= max_batch_size:
        command = ffmpeg_command.generate_for_images(number_images, competitor_images, f"out/batches/out.mp4")
        subprocess.run(command, shell=True)
    else:
        while pictures_done < top_length:
            make_batch(number_images, competitor_images, pictures_done, max_batch_size)
            pictures_done += max_batch_size
        # batches = sorted(glob.glob("out/batches/*"))
        # merge_command = ffmpeg_command.generate_for_videos(batches, "out/top.mp4")
        # subprocess.run(merge_command, shell=True)


def combine_music():
    tracks = glob.glob("out/music/*")

    if os.path.exists("out/music-concat.txt"):
        choise = input("The ffmpeg concat file is already present. Generate anyway? [Y/n]: ")
        if not choise_positive(choise):
            return

    if len(tracks) == 0:
        print("No music found in 'out/music/'. You should copy your tracks manually and try again")
        return

    print("The ffmpeg concat file will be saved as out/music-concat.txt")
    input(f"Found {len(tracks)} track(s). Press Enter to continue...")
    music_concat.concatenate()


def ensure_exist(wildcard: str, name: str) -> bool:
    if len(glob.glob(wildcard)) > 0:
        print(f"[+] {name} - found at '{wildcard}'")
        return True
    else:
        print(f"[-] {name} - not found at '{wildcard}'")
        return False


def render_final_video():
    intro = "out/intro.mp4"
    outro = "out/outro.mp4"
    music_concat = "out/music-concat.txt"
    batches = "out/batches/*"

    if not ensure_exist(intro, "Intro"): return
    if not ensure_exist(outro, "Outro"): return
    if not ensure_exist(music_concat, "Music concat file"): return
    if not ensure_exist(batches, "Video batch(es)"): return

    input("Press Enter to continue...")
    compose_final_video("out/final.mp4")


options = [
    (1, "Render number images", render_number_images),
    (2, "Get image urls by query", get_image_urls),
    (3, "Download images", download_images),
    (4, "Render top video batch(es)", render_top),
    (5, "Combine music into one track", combine_music),
    (6, "Make intro and outro", lambda: print("This step is manual")),
    (7, "Render final video", render_final_video),
]


def choose_option(choise: int):
    found = False
    for option in options:
        if choise == option[0]:
            option[2]()
            found = True
            break

    if not found:
        print(f"No option with index {choise}")


while True:
    print()
    print("Steps:")
    for option in options:
        print(f"{option[0]}. {option[1]}")
    print("Choose option: ", end="")
    choise = int(input())
    print()
    choose_option(choise)
