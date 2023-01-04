import sys
import glob
import os
import re

path = sys.argv[1]
files = glob.glob(path+"*")

for file in files:
    (name, extension) = os.path.splitext(file)
    match = re.findall(r'\d+', name)[0]
    number = int(match)
    name = re.sub(r'\d+', f"{number:010d}", name)
    os.rename(file, f"{name}.{extension}")
