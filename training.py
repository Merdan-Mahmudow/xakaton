
import torch
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset, DataLoader
import pandas as pd

# Загрузка предобученного токенизатора и модели BERT
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=3)  # 3 класса: негатив, нейтраль, позитив

# Датасет
class SentimentDataset(Dataset):
    def __init__(self, texts, labels):
        self.texts = texts
        self.labels = labels

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        encoding = tokenizer(
            self.texts[idx],
            truncation=True,
            padding='max_length',
            max_length=128,
            return_tensors='pt'
        )
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(self.labels[idx], dtype=torch.long)
        }

# Пример загрузки данных
data = pd.read_csv('your_data.csv')  # Данные должны содержать 'text' и 'label' столбцы
train_texts, val_texts, train_labels, val_labels = train_test_split(data['text'].tolist(), data['label'].tolist(), test_size=0.1)

# Создание обучающего и валидационного датасетов
train_dataset = SentimentDataset(train_texts, train_labels)
val_dataset = SentimentDataset(val_texts, val_labels)

# Параметры обучения
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=16,
    evaluation_strategy="epoch",
    logging_dir='./logs',
)

# Trainer для обучения модели
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
)

# Обучение
trainer.train()

# Сохранение модели
model.save_pretrained('./sentiment_model')
tokenizer.save_pretrained('./sentiment_model')


# Загрузка обученной модели и токенизатора
model = BertForSequenceClassification.from_pretrained('./sentiment_model')
tokenizer = BertTokenizer.from_pretrained('./sentiment_model')

def predict_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)
    outputs = model(**inputs)
    prediction = torch.argmax(outputs.logits, dim=1).item()
    labels = {0: 'Негативный', 1: 'Нейтральный', 2: 'Позитивный'}
    return labels[prediction]

# Пример предсказания
text = "Ваш текст для классификации"
print(f"Тональность: {predict_sentiment(text)}")

