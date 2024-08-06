import enum
from app.configurations import parameters
from app.core.enums import EnumBuilder


# Dynamically create the Enum class for Target Languages
TargetLanguages = EnumBuilder.create_enum(
    'TargetLanguages', parameters["target_languages"]
)
