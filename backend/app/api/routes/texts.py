import base64
from typing import Annotated, Any, List, Optional
from app.api.hooks.text_gen import text_generate_GIGACHA_hook, text_openGPT_hook, yagpt_generation_hook
from app.schemas import GIGACHAT_PROMPTS, GIGACHAT_RESPONSE, YAGPT_PROMPTS, OpenAIRequest
from fastapi import APIRouter, File, HTTPException, UploadFile, Depends
from app.s3 import get_url
import openai
from app.core.config import settings

from app.api.deps import (
    CurrentUser,
    SessionDep,
    get_current_active_superuser,
    get_current_user
)

router = APIRouter()

@router.post("/gigachat/")
async def text_generate_GIGACHAT(prompt: GIGACHAT_RESPONSE, token = Depends(get_current_user)) -> Any:
    try:
        req = text_generate_GIGACHA_hook(prompt.model_dump())
        return req["choices"][0]["message"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/opengpt/")
async def text_generate_OPENGPT(session: SessionDep, prompt: str, files: List[UploadFile] = File(...), token = Depends(get_current_user)) -> Any:
    try:
        upload = await get_url(files)
        req = text_openGPT_hook(prompt, upload)
        return req
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/yagpt-lite")
def text_generate_YAGPT(dto: YAGPT_PROMPTS, token = Depends(get_current_user)) -> Any:
    try:
        print(dto)
        response = yagpt_generation_hook(prompt=dto.prompt, stream=dto.stream)
        return response["result"]["alternatives"][0]["message"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/open_ai_request")
async def open_ai_request(token = Depends(get_current_user)):

    client = openai.OpenAI(
        # This is the default and can be omitted
        api_key=settings.OPENAI_API_KEY,
    )
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Say this is a test",
            }
        ],
        model="gpt-3.5-turbo",
    )
    return chat_completion

