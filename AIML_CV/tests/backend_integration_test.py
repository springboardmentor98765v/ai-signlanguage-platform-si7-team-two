import requests

# AI Service URL
url = "http://127.0.0.1:8001/predict"

# Test Image
image_path = "test_images/A.png"
import os

print("Current Working Directory:")
print(os.getcwd())
with open(image_path, "rb") as image:

    files = {
        "file": image
    }

    response = requests.post(url, files=files)

print("Status Code:", response.status_code)
print()

print("Response:")

print(response.json())