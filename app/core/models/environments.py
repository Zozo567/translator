from enum import Enum
from typing import Union


class Stages(Enum):
    LOCAL = 'local'
    PRODUCTION = 'production'
    STAGING = 'staging'
    DEVELOPMENT = 'development'
