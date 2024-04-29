import numpy as np

from app.routes.scrape_routes import scrape_patches
from run import app

import spacy
import json

import torch

from transformers import pipeline, AutoModelForSequenceClassification, TrainingArguments, Trainer, AutoTokenizer

import evaluate


def remove_after_substring(text, substring):
    parts = text.split(substring)
    if len(parts) > 1:
        return parts[0] + substring
    else:
        return text

from datasets import load_dataset

def main():
    # Example League of Legends patch notes dataset
    dataset = {
        'train': [
            {"label": 1, "text": "Buffed champion X's damage output."},  # Positive
            {"label": 0, "text": "Nerfed champion Y's movement speed."},  # Negative
            {"label": 0, "text": "Adjusted item Z's effectiveness."},  # Negative
            {"label": 1, "text": "Fixed several bugs."},  # Positive
        ],
        'test': [
            {"label": 1, "text": "Buffed champion X's damage output."},  # Positive
            {"label": 0, "text": "Nerfed champion Y's movement speed."},  # Negative
            {"label": 0, "text": "Adjusted item Z's effectiveness."},  # Negative
            {"label": 1, "text": "Fixed several bugs."},  # Positive
        ]
        # Add more examples with corresponding labels
    }

    # dataset = load_dataset("yelp_review_full")

    tokenizer = AutoTokenizer.from_pretrained("google-bert/bert-base-cased")

    def tokenize_function(example):
        out = tokenizer(example["text"], padding="max_length", truncation=True)
        out['labels'] = torch.tensor(example["label"])
        return out


    # def tokenize_function(examples):
    #     # return tokenizer(examples["text"], padding="max_length", truncation=True)
    #     tokenized_inputs = tokenizer([example["text"] for example in examples], padding='max_length', truncation=True,
    #                                  return_tensors="pt")
    #     tokenized_inputs["labels"] = torch.tensor([example["label"] for example in examples])
    #     return tokenized_inputs

    # tokenized_datasets = dataset.map(tokenize_function, batched=True)
    tokenized_datasets = {}
    tokenized_datasets['train'] = [tokenize_function(example) for example in dataset['train']] # tokenize_function(dataset['train']) #
    tokenized_datasets['test'] = [tokenize_function(example) for example in dataset['test']] # tokenize_function(dataset['test']) #
    print(tokenized_datasets)

    small_train_dataset = tokenized_datasets["train"] #.shuffle(seed=42).select(range(1000))
    small_eval_dataset = tokenized_datasets["test"] #.shuffle(seed=42).select(range(1000))

    model = AutoModelForSequenceClassification.from_pretrained("google-bert/bert-base-cased", num_labels=2)

    metric = evaluate.load("accuracy")

    def compute_metrics(eval_pred):
        logits, labels = eval_pred
        predictions = np.argmax(logits, axis=-1)
        return metric.compute(predictions=predictions, references=labels)

    training_args = TrainingArguments(output_dir="test_trainer", evaluation_strategy="epoch")

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=small_train_dataset,
        eval_dataset=small_eval_dataset,
        compute_metrics=compute_metrics,
    )

    def compute_loss(model, inputs, return_outputs=False):
        outputs = model(**inputs)
        logits = outputs.logits
        labels = inputs["labels"]
        criterion = torch.nn.CrossEntropyLoss()
        loss = criterion(logits, labels)
        return (loss, outputs) if return_outputs else loss

    trainer.compute_loss = compute_loss

    trainer.train()


def execute_sentiment_analysis():
    output = {'_id': '14.8', 'release_date': 'April 17th, 2024',
              'champions': [{'champion': 'Akali', 'updates': [{'Stats': 'Base health increased to 600 from 570.'}]},
                            {'champion': 'Azir',
                             'updates': [{'Stats': 'Base health regeneration reduced to 3.5 from 5.'}, {
                                 'Arise!': 'Base damage reduced to 50 / 65 / 80 / 95 / 110 from 50 / 67 / 84 / 101 / 118.'}]},
                            {'champion': 'Brand',
                             'updates': [{'Blaze': 'Bug Fix: Can now once again trigger  Dark Harvest.'}]},
                            {'champion': 'Briar', 'updates': [{'Stats': 'Health growth reduced to 95 from 100.'}, {
                                'Head Rush': 'Cast range increased to 475 units from 450.'}, {
                                                                  'Blood Frenzy': 'Bonus attack speed changed to 55 / 65 / 75 / 85 / 95% from 54 / 68 / 82 / 96 / 110%. Bug Fix: Now properly reveals the nearest target while the effects of nearsight.'}]},
                            {'champion': 'Draven', 'updates': [{
                                                                   'Spinning Axe': 'Base damage increased to 45 / 50 / 55 / 60 / 65 from 40 / 45 / 50 / 55 / 60.'}]}]}

    # Convert to array of dictionaries keyed on champion name and value all the patch notes.
    data = []
    data_clean = []
    for champion in output['champions']:
        champ_data = {}
        champ_data_clean = {}
        champ_data[champion['champion']] = []
        champ_data_clean[champion['champion']] = []
        for update in champion['updates']:
            # champ_data[champion['champion']] += next(iter(update.values())) + " "
            champ_data[champion['champion']].append(next(iter(update.values())))
            update_clean = remove_after_substring(next(iter(update.values())), "reduced")
            update_clean = remove_after_substring(update_clean, "increased")
            champ_data_clean[champion['champion']].append(update_clean)
        data.append(champ_data)
        data_clean.append(champ_data_clean)

    # Remove numeric values associated with the changes.
    # For example, when it says "Damaged increased," remove the subsequent "55 / 65 / ..."

    # Execute sentiment analysis
    print('Initializing sentiment pipeline...')
    sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    print('Sentiment pipeline initialized...')
    for champion in data_clean:
        champ = next(iter(champion.keys()))

        for champion_dirty in data:
            if champ in champion_dirty:
                updates = next(iter(champion_dirty.values()))
                print(updates)
                print(sentiment_pipeline(updates))

        updates = next(iter(champion.values()))

        print(updates)
        print(sentiment_pipeline(updates))
        print('------------------------------')

if __name__ == '__main__':
    main()

# HuggingFace Sentiment Analysis

# nlp = spacy.load("en_core_web_md")
# tokens = nlp(output['champions'][0]['updates'][0]['Stats'])
#
# # Features would be champion names.
# # Value would be the patch notes vectorized.
# # Output would be the win rates of each champion?
#
# for token in tokens:
#     print(token.vector)
#     print(token.text, token.has_vector, token.vector_norm, token.is_oov)