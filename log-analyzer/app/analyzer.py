import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Tuple

# Regex pattern to parse log lines
LOG_PATTERN = re.compile(
    r'^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) '
    r'\[(?P<level>[A-Z]+)\] '
    r'(?P<message>.+)$'
)

ALLOWED_LEVELS = {"INFO", "WARNING", "ERROR"}


class LogAnalyzer:
    """
    Parses and analyzes log files in a directory.
    Includes robust handling of malformed lines and missing files.
    """

    def __init__(self, log_dir: Path):
        if not log_dir.exists() or not log_dir.is_dir():
            raise ValueError(f"Log directory does not exist: {log_dir}")
        self.log_dir = log_dir

    def analyze(self) -> Dict:
        """
        Analyze all .log files in the directory.
        Returns a summary dictionary:
            - total_entries
            - level_counts
            - time_range (earliest, latest)
        """
        level_counts = Counter()
        total_entries = 0
        earliest: Optional[datetime] = None
        latest: Optional[datetime] = None

        log_files = list(self.log_dir.glob("*.log"))
        if not log_files:
            raise ValueError(f"No .log files found in directory: {self.log_dir}")

        for log_file in log_files:
            try:
                with open(log_file, "r", encoding="utf-8") as f:
                    for line_num, line in enumerate(f, start=1):
                        parsed = self._parse_line(line.strip())
                        if parsed is None:
                            print(f"Warning: Skipped malformed line {line_num} in {log_file.name}")
                            continue

                        timestamp, level = parsed

                        if level not in ALLOWED_LEVELS:
                            print(f"Warning: Unknown log level '{level}' in line {line_num} of {log_file.name}")
                            continue

                        level_counts[level] += 1
                        total_entries += 1

                        # Update earliest and latest timestamps
                        if earliest is None or timestamp < earliest:
                            earliest = timestamp
                        if latest is None or timestamp > latest:
                            latest = timestamp

            except Exception as e:
                print(f"Warning: Could not read file {log_file.name}: {e}")

        time_range = self._format_time_range(earliest, latest)

        return {
            "total_entries": total_entries,
            "level_counts": dict(level_counts),
            "time_range": time_range
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
            timestamp = datetime.strptime(
                match.group("timestamp"),
                "%Y-%m-%d %H:%M:%S"
            )
            level = match.group("level")
            return timestamp, level
        except ValueError:
            return None

    def _format_time_range(
        self,
        earliest: Optional[datetime],
        latest: Optional[datetime]
    ) -> Optional[Tuple[str, str]]:
        """
        Format earliest and latest timestamps.
        """
        if earliest is None or latest is None:
            return None
        return (
            earliest.strftime("%Y-%m-%d %H:%M:%S"),
            latest.strftime("%Y-%m-%d %H:%M:%S"),
        )
