from pydantic import BaseModel


class YAGPT_PROMPTS(BaseModel):
	prompt: list[dict] | None 
	stream: bool | None = False

class OpenAIRequest(BaseModel):
    model_name: str
    messages: list[dict[str, str]]

class GIGACHAT_PROMPTS(BaseModel):
	role: str
	content: str

class GIGACHAT_RESPONSE(BaseModel):
	messages: list[GIGACHAT_PROMPTS]

class YANDEX_ART_POST(BaseModel):
	prompt: str

class YANDEX_ART_GET(BaseModel):
	id: str

class COMMENT_CLASSIFIER(BaseModel):
	text: str