"""Formatters and formatting."""

from datetime import datetime, timezone


def format_in_utc(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt.replace(tzinfo=timezone.utc)
    elif dt.tzinfo is not timezone.utc:
        dt = dt.astimezone(timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%S") + "Z"
