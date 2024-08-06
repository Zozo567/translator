from app.core.schema import BaseSchema
from app.apps.translator.models import TargetLanguages


class InTranslatorSchema(BaseSchema):
    text: str
    target_language: TargetLanguages


class TranslatorSchema(BaseSchema):
    translation: str
