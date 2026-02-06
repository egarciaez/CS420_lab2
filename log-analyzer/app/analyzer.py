import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Tuple, Iterable

# -------------------- Constants --------------------

TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_GLOB_PATTERN = "*.log"

LOG_PATTERN = re.compile(
    r'^(?P<timestamp>\d{4}-\d{2}-\d{2} '
    r'\d{2}:\d{2}:\d{2}) '
    r'\[(?P<level>[A-Z]+)\] '
    r'(?P<message>.+)$'
)

ALLOWED_LEVELS = {"INFO", "WARNING", "ERROR"}


# -------------------- Log Analyzer --------------------

class LogAnalyzer:
    """
    Parses and analyzes log files in a directory.
    Produces counts by log level and a time range summary.
    """

    def __init__(self, log_dir: Path):
        self._validate_log_dir(log_dir)
        self.log_dir = log_dir

    def analyze(self) -> Dict[str, object]:
        """
        Analyze all .log files in the directory.
        """
        level_counts = Counter()
        timestamps: list[datetime] = []

        for log_file in self._get_log_files():
            self._process_file(log_file, level_counts, timestamps)

        return self._build_summary(level_counts, timestamps)

    # -------------------- Helpers --------------------

    def _get_log_files(self) -> Iterable[Path]:
        log_files = list(self.log_dir.glob(LOG_GLOB_PATTERN))
        if not log_files:
            raise ValueError(f"No .log files found in directory: {self.log_dir}")
        return log_files

    def _process_file(
        self,
        log_file: Path,
        level_counts: Counter,
        timestamps: list[datetime]
    ) -> None:
        try:
            with log_file.open("r", encoding="utf-8") as file:
                for line_num, line in enumerate(file, start=1):
                    self._process_line(
                        line.strip(),
                        log_file.name,
                        line_num,
                        level_counts,
                        timestamps
                    )
        except Exception as exc:
            print(f"Warning: Could not read file {log_file.name}: {exc}")

    def _process_line(
        self,
        line: str,
        filename: str,
        line_num: int,
        level_counts: Counter,
        timestamps: list[datetime]
    ) -> None:
        parsed = self._parse_line(line)
        if parsed is None:
            print(f"Warning: Skipped malformed line {line_num} in {filename}")
            return

        timestamp, level = parsed

        if level not in ALLOWED_LEVELS:
            print(f"Warning: Unknown log level '{level}' in {filename}:{line_num}")
            return

        level_counts[level] += 1
        timestamps.append(timestamp)

    def _parse_line(self, line: str) -> Optional[Tuple[datetime, str]]:
        match = LOG_PATTERN.match(line)
        if not match:
            return None

        try:
            timestamp = datetime.strptime(
                match.group("timestamp"),
                TIMESTAMP_FORMAT
            )
            return timestamp, match.group("level")
        except ValueError:
            return None

    def _build_summary(
        self,
        level_counts: Counter,
        timestamps: list[datetime]
    ) -> Dict[str, object]:
        time_range = self._format_time_range(timestamps)

        return {
            "total_entries": sum(level_counts.values()),
            "level_counts": dict(level_counts),
            "time_range": time_range
        }

    def _format_time_range(
        self,
        timestamps: list[datetime]
    ) -> Optional[Tuple[str, str]]:
        if not timestamps:
            return None

        return (
            min(timestamps).strftime(TIMESTAMP_FORMAT),
            max(timestamps).strftime(TIMESTAMP_FORMAT),
        )

    @staticmethod
    def _validate_log_dir(log_dir: Path) -> None:
        if not log_dir.exists() or not log_dir.is_dir():
            raise ValueError(f"Log directory does not exist: {log_dir}")
