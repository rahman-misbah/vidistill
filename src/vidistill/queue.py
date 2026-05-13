from typing import Optional

from vidistill.config import QUEUE_FILE


def parse_queue() -> list[tuple[str, Optional[str]]]:
    """Parse queue.txt and return a list of (url, name) tuples.

    Returns:
        A list of tuples, where each tuple contains the lecture URL and an optional name.

    Raises:
        FileNotFoundError: If queue.txt does not exist.
    """

    if not QUEUE_FILE.exists():
        raise FileNotFoundError(
            f"{QUEUE_FILE} not found. Please create the file and add lecture URLs."
        )

    lectures = []
    with open(QUEUE_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue  # Skip empty lines and comments

            parts = line.split(",", 1)
            url = parts[0].strip()
            name = parts[1].strip() or None if len(parts) > 1 else None
            lectures.append((url, name))

    return lectures
