import requests
import json
import config

api_key = config.SERPAPI_KEY
request_string = "https://serpapi.com/search.json?engine=yandex_images&text={query}&p={page}&api_key={key}"
query = "shrek"
image_count = 1000

page = 0
count = 0
items: list[dict] = []

while count < image_count:
    response = requests.get(request_string.format(query=query, page=page, key=api_key)).json()
    image_results = response["images_results"]
    position: int = image_results[-1]["position"]
    count = position
    items.extend(image_results)
    page += 1
    print(f"page {page}; count {count}")

    with open("out/backup-image-query.json", "w+") as file:
        result = { "items": items }
        json.dump(result, file)


with open("out/image-query.json", "w+") as file:
    result = { "items": items }
    json.dump(result, file)
