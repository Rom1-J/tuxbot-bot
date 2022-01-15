from typing import Dict

from structured_config import Structure

HAS_MODELS = False


class TestConfig(Structure):
    pass


extra: Dict[str, Dict] = {}
