 весь Бэкнд и обученные модели находятся в папке `backend`

 + добавлена авторизация, нейросети для общения с клиента, анализ тональности из аудио. Для распознования речи использовался (openai/whisper-large-v3-turbo).

для установки зависимостей используйте UV

 ```bash
git clone https://github.com/Merdan-Mahmudow/xakaton.git

cd backend

uv sync

uv run app/train.py

docker compose watch
```


