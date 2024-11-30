from app.api.hooks.video_gen import text_to_video_pyramyd_flow_hook
from fastapi import APIRouter, Depends
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/pyramyd-flow/")
def text_to_video_generate(prompt: str, duration: int, fps: int, token = Depends(get_current_user)):
	req = text_to_video_pyramyd_flow_hook(prompt, duration, fps)
	return req