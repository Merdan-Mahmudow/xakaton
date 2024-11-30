import base64
import json
from typing import Any
from app.api.hooks.image_gen import flux_generation,  replicate_lomography_image_hook, yandex_generation, yandex_image_get
from app.s3 import get_url_base64
from app.schemas import YANDEX_ART_GET, YANDEX_ART_POST
from app.utils import gigachat_token, ya_token
from fastapi import APIRouter, HTTPException, Depends
import requests
from app.core.config import settings
from app.api.deps import get_current_active_superuser, get_current_user



router = APIRouter()



@router.post("/flux-pro/")
async def text_to_image_generate(prompt: str, token = Depends(get_current_user)) -> Any:
	try:
		create_image = flux_generation(prompt)
		return [{"status": "ok", "url": create_image["sample"]}]
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))




@router.post("/ya-art")
async def text_to_image_generate_YA_ART(prompt: YANDEX_ART_POST, token = Depends(get_current_user)) -> Any:
	create_image = yandex_generation(prompt.prompt)
	#if response.status_code == 200:
	#	image_data = response.json()["response"]["image"]
	#	image_bytes = base64.b64decode(image_data)
	#	with open("image.jpeg", "wb") as f:
	#		f.write(image_bytes)
	#	print("Image saved to image.jpeg")
	#else:
	#	print(f"Error: {response.status_code}")
	#	print(response.text)
	
	
	return [{"status": "ok"}, create_image]
	

@router.get("/ya-art-get")
async def yandex_art_image_get(id: str, token = Depends(get_current_user)):
	image = None
	try:
		while True:
			image_data = json.loads(yandex_image_get(id))
			done = image_data["done"]
			if done:
				image = image_data["response"]["image"]
				break
		return await get_url_base64(base64.b64decode(image))
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))
	




@router.get("/test-tokens")
async def test_tokens(token = Depends(get_current_active_superuser)):
	url = "https://iam.api.cloud.yandex.net/iam/v1/tokens"
	
	data = '{"yandexPassportOauthToken": "y0_AgAAAABmxAAHAATuwQAAAAENNOHGAABp3b1cBgJL24ni6Jyq_pRsaHUL6Q"}'
	
	response = requests.post(url, data=data)
	
	return response.json()
	 
@router.post("/lomography")
def replicate_lomograaphy(prompt: str, aspect_ratio: str, output_quality: int, token = Depends(get_current_user)):
	req = replicate_lomography_image_hook(prompt, aspect_ratio, output_quality)
	return req