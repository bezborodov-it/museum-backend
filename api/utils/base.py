from datetime import datetime, timezone
import pytz


def camel_case_to_snake_case(input_str: str) -> str:
    chars = []
    for c_idx, char in enumerate(input_str):
        if c_idx and char.isupper():
            nxt_idx = c_idx + 1
            flag = nxt_idx >= len(input_str) or input_str[nxt_idx].isupper()
            prev_char = input_str[c_idx - 1]
            if prev_char.isupper() and flag:
                pass
            else:
                chars.append("_")
        chars.append(char.lower())
    return "".join(chars)


def str_ekb_to_utc(value: str) -> datetime:
    parsed_time = datetime.fromisoformat(value.replace('Z', ''))
    yekaterinburg_tz = pytz.timezone("Asia/Yekaterinburg")
    localized_time = yekaterinburg_tz.localize(parsed_time)

    return localized_time.astimezone(timezone.utc)

