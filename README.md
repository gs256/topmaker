# topmaker

Python tool for making meme top videos. It gets you through a bunch of steps and at the end you'll get a final top video with your own intro and outro and images queried from Yandex Images.

![alt thumbnail](https://img.youtube.com/vi/vw5MUun6tBU/mqdefault.jpg)

## How does it work?

It makes a video from images and background music using ffmpeg. There are two types of images: number images and competitor images (like in most of the meme tops). Number images are generated using imagemagick and competitor images are downloaded from Yandex Images. The whole top is technically a slideshow with cringy looking transitions.

## Requirements

-   python 3.8+
-   ffmpeg 4.3+
-   imagemagick
-   Comic Sans MS font

## Quick start

### Setup python environment

First, make a copy of this template file:

```console
$ cp .env-template .env
```

Open the .env file and fill in the fields.

Then install the required packages:

-   `python-dotenv`
-   `requests`

## Install required programs

**On Ubuntu**

```console
$ sudo apt install ffmpeg
$ sudo apt install imagemagick
```

**Note:** make sure your ffmpeg version is above 4.3 by typing `ffmpeg -version`. If it's not install a newer version using ppa or snap

### Install Comic Sans MS font

**On Ubuntu**

1. Download the `Comic Sans MS` font .ttf file from anywhere

2. Copy the .ttf file to `~/.fonts/` directory. If the directory doesn't exist create it with `mkdir ~/.fonts`

**Instructions for other distros may be different**

## How to use?

Run the main script:

```console
$ python3 main.py
```

You will be presented with several options:

1. Render images with numbers: "Number 1", "Number 2" etc.

2. Query competitor images from Yandex Images. You can either do this automatically by choosing the corresponding option in terminal or manually using js script in the `./scripts/` directory

3. Download images queried on the previous step

4. Render top video (if the length of the top is greater than a certain amount the video will be split into multiple parts)

5. Combine music into one track. But before that step you'll need to copy all your music into `./out/music/` directory

6. Make intro and outro. This step is manual. You can either make intro and outro videos using other software or use `image_to_video.py` script to make videos from images

7. Render final video (intro + top video(s) + outro)

## License

MIT
