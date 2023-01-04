import requests
import json
import imghdr

file_path = "dump.json"
image_path_template = "./query_images/img_{number}.{extension}"

items: list[dict] = []

with open(file_path) as file:
    data = json.load(file)
    items = data["items"]

for item in items:
    url = item["thumbnail"]
    response = requests.get(url)
    if response.status_code >= 400:
        raise Exception(f"Status code: {response.status_code}")
    extension = imghdr.what(file=None, h=response.content)
    position = item["position"]
    save_path = image_path_template.format(number=position, extension=extension)
    with open(save_path, 'wb') as f:
        f.write(response.content)
    print(f"Downloaded {position}/{len(items)}")
