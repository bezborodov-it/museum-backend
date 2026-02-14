from sqlalchemy import case, literal_column
from typing import List, Tuple
from api.models.enum import AgeEnum

def build_age_priority_and_allowed(
    age_column,
    selected_ages: List[AgeEnum]
) -> Tuple[any, List[AgeEnum] | None]:
    if not selected_ages:
        return literal_column("0"), None

    age_order_desc = [
        AgeEnum.EIGHTEEN_PLUS,
        AgeEnum.SIXTEEN_PLUS,
        AgeEnum.FOURTEEN_PLUS,
        AgeEnum.TWELVE_PLUS,
        AgeEnum.SIX_PLUS,
        AgeEnum.ZERO_PLUS,
    ]

    # Находим все разрешённые возраста (union диапазонов)
    allowed_set = set()
    for sel in selected_ages:
        idx = age_order_desc.index(sel)
        allowed_set.update(age_order_desc[idx:])  # добавляем sel и всё младше

    allowed_ages = [a for a in age_order_desc if a in allowed_set]  # сохраняем порядок

    # Выбранные сортируем по строгости (от строгого к мягкому)
    selected_sorted = sorted(selected_ages, key=lambda a: age_order_desc.index(a))

    # Остальные разрешённые (не выбранные пользователем)
    remaining = [a for a in allowed_ages if a not in selected_ages]

    # Итоговый порядок: выбранные → остальные разрешённые
    priority_order = selected_sorted + remaining

    whens = [(age_column == age, i) for i, age in enumerate(priority_order)]
    age_priority = case(*whens, else_=999)

    return age_priority, allowed_ages
