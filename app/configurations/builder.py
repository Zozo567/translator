import json
from os import getenv
from typing import Union
from app.core.models.environments import Stages

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


class Parameters:
    """ Class which stands for managing application parameters stored in .env file """

    __stage_key_in_environment_file = 'STAGE'
    __target_languages_key = 'TARGET_LANGUAGES'
    __source_language = 'SOURCE_LANGUAGE'

    __available_stages = [stage.value for stage in Stages]

    def __init__(self) -> None:
        self.application_stage = getenv(
            self.__stage_key_in_environment_file, None
        )
        self.application_stage = None if self.application_stage is None else self.application_stage.lower()
        self.source_language = getenv(self.__source_language, None)
        self.target_languages = getenv(self.__target_languages_key, None)

    def __check_environment_variables_not_none(self):
        environmnets = [
            self.source_language,
            self.application_stage,
            self.target_languages
        ]

        if any(value is None for value in environmnets):
            raise EnvironmentError(
                f'Environmental variales are missing. Check: {environmnets}')
        return

    def __identify_stage_in_environment(self) -> Union[None, EnvironmentError]:
        try:
            self.application_stage = Stages(
                self.application_stage)     # Stages.production
            self.application_stage = self.application_stage.value       # production
            return

        except ValueError:
            message = f'Unsupported "STAGE" value {self.application_stage} provided in .env file. \
                        Supported stages: {self.__available_stages}'
            raise EnvironmentError(message)

    def __call__(self):
        self.__check_environment_variables_not_none()
        self.__identify_stage_in_environment()

        return {
            "stage": self.application_stage,
            "source_language": self.source_language,
            "target_languages": json.loads(self.target_languages),
        }


class Models:
    def __init__(self, parameters: dict) -> None:
        self.parameters = parameters

    def load_model(self, target_lang: str):
        """
        Loads the translation model and tokenizer for the specified target language.

        Parameters:
        target_lang (str): The target language code (e.g., 'es' for Spanish).

        Returns:
        (AutoTokenizer, AutoModelForSeq2SeqLM): The tokenizer and model for the specified language.
        """
        model_name = f"Helsinki-NLP/opus-mt-{self.parameters['source_language']}-{target_lang}"

        # For Portuguese need to load another model
        if target_lang == "pt":
            model_name = f"Helsinki-NLP/opus-mt-tc-big-{self.parameters['source_language']}-{target_lang}"

        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

        return tokenizer, model
