import random
import glob
from os import path


def concatenate():
    output = "out/music-concat.txt"
    music_path = "out/music/"

    music = glob.glob(music_path+"*")
    random.shuffle(music)

    with open(output, "w+") as file:
        for item in music:
            file.write(f"file 'music/{path.basename(item)}'\n")
