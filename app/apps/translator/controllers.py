from fastapi import APIRouter, status

from app.apps.translator.services import TranslatorService
from app.apps.translator.schema import TranslatorSchema, InTranslatorSchema

translator_router = APIRouter()


@translator_router.post(
    "",
    response_model=TranslatorSchema,
    status_code=status.HTTP_200_OK,
    summary="Translate text",
    description="""Translate text from English to chosen target language: 
        "ES" - Spanish,
        "DE" - German,
        "FR" - French,
        "JA" - Japanese,
        "AR" - Arabic,
        "HI" - Hindi,
        "PT" - Portuguese, 
        "HU" - Hungarian
    """
)
async def translate(
    translator_schema: InTranslatorSchema
):
    return await TranslatorService().translate(translator_schema)
