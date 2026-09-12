from datetime import datetime
from pathlib import Path


LOG_DIR = Path("log")


def _write_log(filename: str, message: str):
    """Write a timestamped message to a log file."""

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().isoformat()

    with (LOG_DIR / filename).open("a", encoding="utf-8") as file:
        file.write(f"{timestamp} | {message}\n")


def log_activity(user_id: int, action: str):
    """Record an activity performed by a user."""

    _write_log(
        "activity_log.txt",
        f"User {user_id} {action}",
        )


def update_calendar(user_id: int, message: str):
    """Record a calendar update associated with a user's task."""

    _write_log(
        "calendar_log.txt",
        f"User {user_id} | {message}",
        )
