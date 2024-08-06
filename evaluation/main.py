from datasets import load_dataset
import sacrebleu
import csv
import time
from datetime import datetime

from app.configurations.builder import (
    Parameters,
    Models
)
API_PREFIX = '/api/v1'

parameters = Parameters().__call__()


dataset_en_es = load_dataset('opus100', 'en-es')
dataset_en_fr = load_dataset('wmt14', 'fr-en')
dataset_en_de = load_dataset('wmt14', 'de-en')
dataset_en_ja = load_dataset('opus100', 'en-ja')
dataset_en_ar = load_dataset('opus100', 'ar-en')
dataset_en_hi = load_dataset('opus100', 'en-hi')
dataset_en_pt = load_dataset('opus100', 'en-pt')

datasets = {
    "es": dataset_en_es,
    "fr": dataset_en_fr,
    "de": dataset_en_de,
    "ja": dataset_en_ja,
    "ar": dataset_en_ar,
    "hi": dataset_en_hi,
    "pt": dataset_en_pt
}


models = {}

# Load models and tokenizers for all target languages
for language in parameters["target_languages"]:
    tokenizer, model = Models(parameters).load_model(language)
    models[language] = {
        "tokenizer": tokenizer,
        "model": model
    }


def evaluate_model(dataset, model, tokenizer, source_lang, target_lang, num_samples=100):
    # Prepare source and reference texts
    translations_data = dataset['test']['translation'][:num_samples]
    source_texts = [item[source_lang] for item in translations_data]
    reference_texts = [item[target_lang] for item in translations_data]

    # Translate source texts
    translations = []
    for text in source_texts:
        inputs = tokenizer(text, return_tensors="pt",
                           truncation=True, padding=True, max_length=512)
        outputs = model.generate(**inputs)
        translation = tokenizer.decode(outputs[0], skip_special_tokens=True)
        translations.append(translation)

    # Calculate BLEU score
    bleu = sacrebleu.corpus_bleu(translations, [reference_texts])
    return bleu.score


results = []
for lang in parameters["target_languages"]:
    print(f"Evaluating {lang}...")
    bleu_score = evaluate_model(
        datasets[lang],
        models[lang]["model"],
        models[lang]["tokenizer"],
        parameters["source_language"],
        lang
    )
    results.append({
        "language_pair": lang,
        "bleu_score": bleu_score
    })


# Get current timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Define the CSV file name
csv_file_name = f"bleu_score_{timestamp}.csv"

# Write results to CSV
with open(csv_file_name, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["language_pair", "bleu_score"])
    writer.writeheader()
    for result in results:
        writer.writerow(result)
