from app.api.hooks.analyze import get_max_sentiment, predict_sentiment, text_translate
from app.schemas import COMMENT_CLASSIFIER
from fastapi import APIRouter, File, HTTPException, UploadFile
import requests
import torch
from transformers import BertTokenizer, BertForSequenceClassification



router = APIRouter()

@router.post('/')
def comment_classifier(dto: COMMENT_CLASSIFIER):
    text = dto.text
    translated_text = text_translate(text)
    sentiment_results = predict_sentiment(translated_text)
    max_sentiment = get_max_sentiment(sentiment_results)
    return {"label": max_sentiment,
                "text": text}

@router.post('/audio')
async def speech_recognition(file: UploadFile = File(...)):
    try:
        f = await file.read()
        API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3-turbo"
        headers = {"Authorization": "Bearer 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"}

        response = requests.post(API_URL, headers=headers, data=f)
        response.raise_for_status()
        text = response.json()["text"]
        translated_text = text_translate(text)
        sentiment_results = predict_sentiment(translated_text)
        max_sentiment = get_max_sentiment(sentiment_results)

        return {"label": max_sentiment,
                "text": text}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error with Hugging Face API: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

# Загрузка обученной модели и токенизатора
model = BertForSequenceClassification.from_pretrained('/home/softp04/Рабочий стол/full-stack/backend/sentiment_model')
tokenizer = BertTokenizer.from_pretrained('/home/softp04/Рабочий стол/full-stack/backend/sentiment_model')

def predict_sentiment_old(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)
    outputs = model(**inputs)
    prediction = torch.argmax(outputs.logits, dim=1).item()
    labels = {0: 'Негативный', 1: 'Нейтральный', 2: 'Позитивный'}
    return str([labels[prediction], str(prediction), str(outputs), str(inputs)])

@router.post('/old')
def comment_classifier(text: str) -> str:
    return predict_sentiment_old(text)
