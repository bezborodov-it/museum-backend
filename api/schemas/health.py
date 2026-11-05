from typing import Optional, List, Union
from datetime import datetime
from pydantic import BaseModel, field_serializer
from enum import StrEnum


class HealthStatusEnum(StrEnum):
    OK = "ok"
    MAINTENANCE = "maintenance"

class HealthStatus(BaseModel):
    status: HealthStatusEnum
    version: str
