"""Formatters and formatting."""

from datetime import datetime, timezone


def format_in_utc(dt: datetime) -> str:
    """Format a datetime to a string in UTC.

    Args:
        dt (datetime): A datetime object.

    Returns:
        str: The datetime format as a string.
    """
    if dt.tzinfo is None:
        dt.replace(tzinfo=timezone.utc)
    elif dt.tzinfo is not timezone.utc:
        dt = dt.astimezone(timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%S") + "Z"
