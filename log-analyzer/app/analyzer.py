import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Regex pattern to parse log lines
LOG_PATTERN = re.compile(
    r'^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) '
    r'\[(?P<level>[A-Z]+)\] '
    r'(?P<message>.+)$'
)


class LogAnalyzer:
    """
    Parses and analyzes log files in a directory.
    """

    def __init__(self, log_dir: Path):
        if not log_dir.exists() or not log_dir.is_dir():
            raise ValueError(f"Log directory does not exist: {log_dir}")
        self.log_dir = log_dir

    def analyze(self) -> Dict:
        """
        Analyze all .log files in the directory.
        Returns a summary dictionary with:
            - total_entries
            - level_counts
            - time_range (earliest, latest)
        """
        timestamps: List[datetime] = []
        level_counts = Counter()
        total_entries = 0

        # Iterate through all .log files
        for log_file in self.log_dir.glob("*.log"):
            with open(log_file, "r", encoding="utf-8") as f:
                for line in f:
                    parsed = self._parse_line(line.strip())
                    if parsed is None:
                        continue  # Skip malformed lines
                    timestamp, level = parsed
                    timestamps.append(timestamp)
                    level_counts[level] += 1
                    total_entries += 1

        return {
            "total_entries": total_entries,
            "level_counts": dict(level_counts),
            "time_range": self._calculate_time_range(timestamps)
        }

    def _parse_line(self, line: str) -> Optional[Tuple[datetime, str]]:
        """
        Parse a single log line.
        Returns (timestamp, level) or None if invalid.
        """
        match = LOG_PATTERN.match(line)
        if not match:
            return None
        try:
            timestamp = datetime.strptime(match.group("timestamp"), "%Y-%m-%d %H:%M:%S")
            level = match.group("level")
            return timestamp, level
        except ValueError:
            return None

    def _calculate_time_range(self, timestamps: List[datetime]) -> Optional[Tuple[str, str]]:
        """
        Returns the earliest and latest timestamps as ISO strings, or None if no timestamps.
        """
        if not timestamps:
            return None
        return min(timestamps).isoformat(), max(timestamps).isoformat()

