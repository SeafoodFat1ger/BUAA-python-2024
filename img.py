import requests

client_id = "46b19cb33808ad4"


def upload_image_to_imgur(image_path):
    url = "https://api.imgur.com/3/image"
    headers = {"Authorization": f"Client-ID {client_id}"}
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
    response = requests.post(url, headers=headers, files={"image": image_data})
    if response.status_code == 200:
        return response.json()["data"]["link"]
    else:
        raise Exception("Failed to upload image: " + response.json()["data"]["error"])
