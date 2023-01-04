import requests
import json

api_key = ""
request_string = "https://serpapi.com/search.json?engine=yandex_images&text={query}&p={page}&api_key={key}"

page = 0
count = 0
items: list[dict] = []

while count < 1000:
    response = requests.get(request_string.format(query="shrek", page=page, key=api_key)).json()
    image_results = response["images_results"]
    position: int = image_results[-1]["position"]
    count = position
    items.extend(image_results)
    page += 1
    print(f"page {page}; count {count}")

    with open("temp-dump.json", "w+") as file:
        result = { "items": items }
        json.dump(result, file)


with open("dump.json", "w+") as file:
    result = { "items": items }
    json.dump(result, file)
