from sqlalchemy import case, cast, String
from typing import List
from api.models.enum import AgeEnum

AGE_ORDER = [
    AgeEnum.ZERO_PLUS,
    AgeEnum.SIX_PLUS,
    AgeEnum.TWELVE_PLUS,
    AgeEnum.FOURTEEN_PLUS,
    AgeEnum.SIXTEEN_PLUS,
    AgeEnum.EIGHTEEN_PLUS,
]


def build_age_priority(selected: List[AgeEnum]) -> List[AgeEnum]:
    if not selected:
        return AGE_ORDER

    selected_sorted = sorted(
        selected, key=lambda a: AGE_ORDER.index(a), reverse=True
    )

    rest = [a for a in AGE_ORDER if a not in selected]
    rest_sorted = sorted(
        rest, key=lambda a: AGE_ORDER.index(a), reverse=True
    )

    return selected_sorted + rest_sorted


def build_age_case(model_age_column, selected_ages: List[AgeEnum]):
    """
    Возвращает sqlalchemy.case с кастом для Postgres ENUM
    """
    ordered = build_age_priority(selected_ages)

    # каст ENUM в VARCHAR
    age_as_text = cast(model_age_column, String)

    return case(
        {age.value: i for i, age in enumerate(ordered)},
        value=age_as_text,
        else_=100,
    )
