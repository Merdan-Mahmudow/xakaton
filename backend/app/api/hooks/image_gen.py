import json
import time
from app.utils import ya_token
import requests
from app.core.config import settings

def flux_image_get(id: str):
      result = requests.get(
            'https://api.bfl.ml/v1/get_result',
            headers={
                'accept': 'application/json',
                'x-key': "ae5255f1-7094-4ac3-a50b-cc333fb05f14",
            },
            params={
                'id': id
            },
        ).json()
      return result

def flux_generation(prompt: str):
    request = requests.post(
        'https://api.bfl.ml/v1/flux-pro-1.1',
        headers={
            'accept': 'application/json',
            'x-key': "ae5255f1-7094-4ac3-a50b-cc333fb05f14",
            'Content-Type': 'application/json',
        },
        json={
            'prompt': prompt,
            'width': 1024,
            'height': 768,
        },
    ).json()
    print(request)
    request_id = request["id"]
    done = False
    while True:
        response = flux_image_get(request_id)
        if not response["result"]:
            time.sleep(1)
        else:
            done = True
            break
    if done:
        return response["result"]


def yandex_generation(prompt: str):
	url = "https://llm.api.cloud.yandex.net/foundationModels/v1/imageGenerationAsync"
	iamToken = ya_token()
	
	headers = {
		"Authorization": f"Bearer {iamToken}"
	}
	
	data = {
"modelUri": f"art://{settings.YANDEX_FOLDER_ID}/yandex-art/latest",
"generationOptions": {
  "seed": "1863",
  "aspectRatio": {
     "widthRatio": "3",
     "heightRatio": "4"
   }
},
"messages": [
  {
    "weight": "1",
    "text": prompt
  }
]
}
	response = requests.post(url, headers=headers, data=json.dumps(data))
	return response.json()


def yandex_image_get(id: str):
	iamToken = ya_token()
	operation_id = id
	url = f"https://llm.api.cloud.yandex.net:443/operations/{operation_id}"
	headers = {
		"Authorization": f"Bearer {iamToken}"
	}
	response = requests.get(url, headers=headers)
	return response.text

def replicate_lomography_image_hook(prompt: str, aspect_ratio: str, output_quality: int):
	url = "https://api.replicate.com/v1/predictions"
	
	headers = {
		"Authorization": f"Bearer {settings.REPLICATE_API_TOKEN}",
		"Content-Type": "application/json",
		"Prefer": "wait"
	}
	
	data = {
		"version": "3e4d07d16e49be22c9158b6e4864d54c3fb6f676353d49c26c0646771703ddd5",
		"input": {
			"prompt": prompt,
			"aspect_ratio": aspect_ratio,
			"output_quality": output_quality | 80
		}
	}
	
	response = requests.post(url, headers=headers, data=json.dumps(data))
	
	return response.json()
