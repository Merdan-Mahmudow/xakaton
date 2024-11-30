import json
from typing import Annotated, Any, List, Optional
from app.utils import gigachat_token
import requests
from fastapi import File, UploadFile
from gradio_client import Client, handle_file
from app.core.config import settings






def text_generate_GIGACHA_hook(prompt) -> Any:
    access_token = gigachat_token()

    url = 'https://gigachat.devices.sberbank.ru/api/v1/chat/completions'

    payload = json.dumps({
        "model": "GigaChat",
        "messages": prompt["messages"],
        "functional_call": "auto"
    })
    print(payload)
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)

    print(response.text)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code}"
    
def text_openGPT_hook(prompt: str, files: list | None = None):
	client = Client("KingNish/OpenGPT-4o")
	result = client.predict(
			user_prompt={"text": prompt,"files": files},
			api_name="/chat",
	)
	return result


def yagpt_generation_hook(prompt: list[dict], stream: bool | None = False):
    payload = json.dumps({
        "modelUri": f"gpt://{settings.YANDEX_FOLDER_ID}/yandexgpt-lite",
        "completionOptions": {
            "stream": stream,
			"temperature": 0.6,
			"maxTokens": "3000",
		},
        "messages": prompt
	})
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Authorization": f"Api-Key {settings.YANDEX_API_SECRET}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, data=payload)
    return response.json()