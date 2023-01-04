from os import popen
import subprocess

TEMPLATE = "convert -background {bg} -fill {fill} -size {w}x{h} -gravity center -pointsize {pointsize} -font Comic-Sans-MS 'caption:{text}' ./number_images/img-{number}.png"

count = 1000

for i in range(count):
    number = i + 1
    command = TEMPLATE.format(bg="DodgerBlue", fill="white", w=854, h=480, pointsize=60, text=f"Number {number}", number=number)
    subprocess.run(command, shell=True)
