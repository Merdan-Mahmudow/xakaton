from app.core.config import settings
import requests
import json
from gradio_client import Client, handle_file


def text_to_video_pyramyd_flow_hook(prompt: str, duration: int, fps: int):
	#url = "https://api.replicate.com/v1/predictions"

	#headers = {
	#	"Authorization": f"Bearer {settings.REPLICATE_API_TOKEN}",
	#	"Content-Type": "application/json",
	#	"Prefer": "wait"
	#}

	#data = {
	#	"version": "8e221e66498a52bb3a928a4b49d85379c99ca60fec41511265deec35d547c1fb",
	#	"input": {
	#		"prompt": prompt,
	#		"duration": duration,
	#		"frames_per_second": fps
	#	}
	#}

	#response = requests.post(url, headers=headers, data=json.dumps(data))

	#return response.json()

	client = Client("Pyramid-Flow/pyramid-flow")
	result = client.predict(
			prompt="Hello!!",
			image=None,
			duration=3,
			guidance_scale=9,
			video_guidance_scale=5,
			frames_per_second=8,
			api_name="/generate_video",
	)
	return result