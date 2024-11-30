import numpy as np
from scipy.special import softmax
from transformers import AutoModelForSequenceClassification, AutoTokenizer, AutoConfig

def preprocess(text):
    return " ".join(['@user' if t.startswith('@') and len(t) > 1 else 'http' if t.startswith('http') else t for t in text.split()])

MODEL = "/home/softp04/Рабочий стол/full-stack/backend/app/roberta" # Using a publicly available model
tokenizer = AutoTokenizer.from_pretrained(MODEL)
config = AutoConfig.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

def predict_sentiment(text):
    text = preprocess(text)
    encoded_input = tokenizer(text, return_tensors='pt')
    output = model(**encoded_input)
    scores = output.logits[0].detach().numpy()
    scores = softmax(scores)

    ranking = np.argsort(scores)[::-1]
    results = []
    for i in range(scores.shape[0]):
        label = config.id2label[ranking[i]]
        score = scores[ranking[i]]
        label_mapping = {"negative": "Негативный", "neutral": "Нейтральный", "positive": "Позитивный"}
        results.append({
            "label": label_mapping.get(label, label),  # Use the mapping or fallback to original
            "score": int(round(score * 100))
        })
    return results


def get_max_sentiment(results):
    return max(results, key=lambda x: x['score'])['label']


text = "Very bad university"

sentiment_results = predict_sentiment(text)
max_sentiment = get_max_sentiment(sentiment_results)
print(max_sentiment)



