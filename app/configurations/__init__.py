import logging
from app.core.models.environments import Stages

from app.configurations.builder import (
    Parameters,
    Models
)

logging.basicConfig(level=logging.INFO)

API_PREFIX = '/api/v1'

parameters = Parameters().__call__()


models = {}

# Load models and tokenizers for all target languages
for language in parameters["target_languages"]:
    logging.info(f"Loading model for language: {language}")
    tokenizer, model = Models(parameters).load_model(language)
    models[language] = {
        "tokenizer": tokenizer,
        "model": model
    }
