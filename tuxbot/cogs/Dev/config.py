from typing import Dict

from structured_config import Structure

HAS_MODELS = False


class DevConfig(Structure):
    pass


extra: Dict[str, Dict] = {}
