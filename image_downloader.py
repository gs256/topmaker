import requests
import json
import imghdr
import os


def download(max_count: int):
    file_path = "out/image-query.json"
    image_path_template = "out/competitors/img_{number}.{extension}"

    items: list[dict] = []

    with open(file_path) as file:
        data = json.load(file)
        items = data["items"]

    os.makedirs("out/competitors", exist_ok=True)
    downloaded_count = 0

    for item in items:
        if max_count != 0 and downloaded_count >= max_count:
            return

        url = item["thumbnail"]
        response = requests.get(url)

        if response.status_code >= 400:
            raise Exception(f"Status code: {response.status_code}")

        extension = imghdr.what(file=None, h=response.content)
        position = item["position"]
        save_path = image_path_template.format(number=f"{position:010d}", extension=extension)

        with open(save_path, 'wb') as f:
            f.write(response.content)

        downloaded_count += 1
        print(f"Downloaded {position}/{len(items)}")
