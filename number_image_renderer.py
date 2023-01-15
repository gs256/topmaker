import os
import subprocess
import config

# for a background picture instead of a solid color
# TEMPLATE = "convert out/bg.png -fill {fill} -resize {w}x{h}\! -gravity center -pointsize {pointsize} -font Comic-Sans-MS -annotate 0 '{text}' {out}"

TEMPLATE = "convert -background {bg} -fill {fill} -size {w}x{h} -gravity center -pointsize {pointsize} -font Comic-Sans-MS 'caption:{text}' {out}"

def render(count: int):
    global TEMPLATE
    bg_color = "SeaGreen3"

    os.makedirs("out/numbers", exist_ok=True)

    for i in range(count):
        number = i + 1
        out = f"./out/numbers/img_{number:010d}.jpg"
        command = TEMPLATE.format(bg=bg_color, fill="white", w=config.WIDTH, h=config.HEIGHT, pointsize=60, text=f"Number {number}", out=out)
        subprocess.run(command, shell=True)
