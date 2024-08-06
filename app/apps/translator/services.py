import re
from app.apps.translator.schema import InTranslatorSchema, TranslatorSchema
from app.configurations import models


class TranslatorService:
    def __init__(self):
        pass

    async def translate(
        self, in_translator_schema: InTranslatorSchema
    ) -> TranslatorSchema:
        language = in_translator_schema.target_language.name
        text = in_translator_schema.text

        model = models[language]["model"]
        tokenizer = models[language]["tokenizer"]

        # Extract bracketed text and replace with placeholders
        bracketed_texts = re.findall(r'\[.*?\]', text)
        placeholder_text = text
        for i, bracketed_text in enumerate(bracketed_texts):
            placeholder_text = placeholder_text.replace(
                bracketed_text, f"<placeholder{i}>")

        # Encode the text with placeholders
        inputs = tokenizer.encode(
            placeholder_text, return_tensors="pt", truncation=True)

        # Generate the translation
        outputs = model.generate(inputs, num_beams=4, early_stopping=True)

        # Decode the output
        translated_placeholder_text = tokenizer.decode(
            outputs[0], skip_special_tokens=True)

        # Replace placeholders with original bracketed text
        for i, bracketed_text in enumerate(bracketed_texts):
            translated_placeholder_text = translated_placeholder_text.replace(
                f"<placeholder{i}>", bracketed_text)

        return TranslatorSchema(translation=translated_placeholder_text)
