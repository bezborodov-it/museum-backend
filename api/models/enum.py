from enum import StrEnum

class AgeEnum(StrEnum):
    ZERO_PLUS = "ZERO_PLUS"
    SIX_PLUS = "SIX_PLUS"
    TWELVE_PLUS = "TWELVE_PLUS"
    FOURTEEN_PLUS = "FOURTEEN_PLUS"
    SIXTEEN_PLUS = "SIXTEEN_PLUS"
    EIGHTEEN_PLUS = "EIGHTEEN_PLUS"

    @property
    def display_name(self) -> str:
        mapping = {
            "ZERO_PLUS": "0+",
            "SIX_PLUS": "6+",
            "TWELVE_PLUS": "12+",
            "FOURTEEN_PLUS": "14+",
            "SIXTEEN_PLUS": "16+",
            "EIGHTEEN_PLUS": "18+",
        }
        return mapping[self.value]

class ActivityTypeEnum(StrEnum):
    EXHIBITION = "EXHIBITION"
    EVENT = "EVENT"