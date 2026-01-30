import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

LOG_PATTERN = re.compile(
    r'^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) '
    r'\[(?P<level>[A-Z]+)\] '
    r'(?P<message>.+)$'
)

class LogAnalyzer:
    """
    Encapsulates all logic related to parsing and analyzing log files.
    Designed to be reusable and testable independent of the CLI.
    """

    def __init__(self, log_dir: Path):
        if not log_dir.exists() or not log_dir.is_dir():
            raise ValueError(f"Log directory does not exist: {log_dir}")
        self.log_dir = log_dir

    def analyze(self) -> Dict:
        timestamps: List[datetime] = []
        level_counts = Counter()
        total_entries = 0

        for log_file in self.log_dir.glob("*.log"):
            self._process_file(
                log_file,
                timestamps,
                level_counts,
                lambda: self._increment_total(total_entries)
            )
            with open(log_file, "r") as f:
                for line in f:
                    parsed = self._parse_line(line.strip())
                    if not parsed:
                        continue

                    timestamp, level = parsed
                    timestamps.append(timestamp)
                    level_counts[level] += 1
                    total_entries += 1

        return {
            "total_entries": total_entries,
            "level_counts": dict(level_counts),
            "time_range": self._calculate_time_range(timestamps)
        }

    def _parse_line(self, line: str) -> Tuple[datetime, str] | None:
        match = LOG_PATTERN.match(line)
        if not match:
            return None

        try:
            timestamp = datetime.strptime(
                match.group("timestamp"),
                "%Y-%m-%d %H:%M:%S"
            )
            level = match.group("level")
            return timestamp, level
        except ValueError:
            return None

    def _calculate_time_range(self, timestamps: List[datetime]) -> Tuple[str, str] | None:
        if not timestamps:
            return None
        return min(timestamps).isoformat(), max(timestamps).isoformat()
