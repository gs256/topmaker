import os
import subprocess
import config

TEMPLATE = "convert -background {bg} -fill {fill} -size {w}x{h} -gravity center -pointsize {pointsize} -font Comic-Sans-MS 'caption:{text}' {out}"

count = 10

os.makedirs("out/numbers", exist_ok=True)

for i in range(count):
    number = i + 1
    out = f"./out/numbers/img_{number:010d}.png"
    command = TEMPLATE.format(bg="DodgerBlue", fill="white", w=config.WIDTH, h=config.HEIGHT, pointsize=60, text=f"Number {number}", out=out)
    subprocess.run(command, shell=True)
