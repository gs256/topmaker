import requests
import json
import imghdr
import os

file_path = "out/image-query.json"
image_path_template = "out/competitors/img_{number}.{extension}"

items: list[dict] = []

with open(file_path) as file:
    data = json.load(file)
    items = data["items"]

os.makedirs("out/competitors", exist_ok=True)

for item in items:
    url = item["thumbnail"]
    response = requests.get(url)
    if response.status_code >= 400:
        raise Exception(f"Status code: {response.status_code}")
    extension = imghdr.what(file=None, h=response.content)
    position = item["position"]
    save_path = image_path_template.format(number=f"{position:010d}", extension=extension)
    with open(save_path, 'wb') as f:
        f.write(response.content)
    print(f"Downloaded {position}/{len(items)}")
