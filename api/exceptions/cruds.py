from typing import Any


class NotFoundError(Exception):
    def __init__(self, model: str, field: str, value: Any):
        self.model = model
        self.field = field
        self.value = value
