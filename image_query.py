import requests
import json
import config


def query(search: str, image_count: int):
    api_key = config.SERPAPI_KEY
    request_string = "https://serpapi.com/search.json?engine=yandex_images&text={query}&p={page}&api_key={key}"

    page = 0
    count = 0
    items: list[dict] = []

    while count < image_count:
        response = requests.get(request_string.format(query=search, page=page, key=api_key)).json()
        image_results = response["images_results"]
        position: int = image_results[-1]["position"]

        for image_result in image_results:
            image_result["page"] = page

        count = position
        items.extend(image_results)
        page += 1
        print(f"page {page}; count {count}")

        with open("out/image-query.json", "w+") as file:
            result = { "items": items }
            json.dump(result, file)


    with open("out/image-query-backup.json", "w+") as file:
        result = { "items": items }
        json.dump(result, file)
