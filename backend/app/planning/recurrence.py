import re
from datetime import UTC, datetime, timedelta
from zoneinfo import ZoneInfo

from dateutil.rrule import rrulestr

from app.agent.errors import AgentError

ALLOWED_FIELDS = {
    "FREQ",
    "INTERVAL",
    "BYDAY",
    "BYMONTHDAY",
    "BYMONTH",
    "BYHOUR",
    "BYMINUTE",
    "COUNT",
    "UNTIL",
}


def rule(text: str, start: datetime, timezone: str):
    try:
        parts = text.upper().removeprefix("RRULE:").split(";")
        fields = {}
        for part in parts:
            key, value = part.split("=", 1)
            if key not in ALLOWED_FIELDS or key in fields or len(value.split(",")) > 8:
                raise ValueError()
            if not re.fullmatch(r"[A-Z0-9,+-]+", value):
                raise ValueError()
            fields[key] = value
        if fields.get("FREQ") not in {"DAILY", "WEEKLY", "MONTHLY", "YEARLY"}:
            raise ValueError()
        if "COUNT" in fields and ("UNTIL" in fields or not 1 <= int(fields["COUNT"]) <= 10000):
            raise ValueError()
        if not 1 <= int(fields.get("INTERVAL", 1)) <= 100:
            raise ValueError()
        return rrulestr(
            ";".join(f"{key}={value}" for key, value in fields.items()),
            dtstart=start.astimezone(ZoneInfo(timezone)),
            cache=False,
        )
    except (ValueError, TypeError, OverflowError, KeyError):
        raise AgentError("invalid_recurrence", 422) from None


def first_occurrence(text: str | None, start: datetime, timezone: str) -> datetime:
    if not text:
        return start.astimezone(UTC)
    occurrence = rule(text, start, timezone).after(
        start.astimezone(ZoneInfo(timezone)) - timedelta(microseconds=1)
    )
    if occurrence is None:
        raise AgentError("recurrence_has_no_occurrence", 422)
    return occurrence.astimezone(UTC)


def next_occurrence(
    text: str | None, start: datetime, timezone: str, after: datetime
) -> datetime | None:
    if not text:
        return None
    result = rule(text, start, timezone).after(after.astimezone(ZoneInfo(timezone)))
    return result.astimezone(UTC) if result else None
