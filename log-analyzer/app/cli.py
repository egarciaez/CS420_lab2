import argparse
from pathlib import Path
from analyzer import LogAnalyzer

def print_report(report: dict):
    print("\n📊 Log Analysis Summary")
    print("-" * 30)
    print(f"Total log entries: {report['total_entries']}")

    if report["time_range"]:
        start, end = report["time_range"]
        print(f"Time range: {start} → {end}")
    else:
        print("Time range: No valid timestamps found")

    print("\nLog Levels:")
    for level, count in report["level_counts"].items():
        print(f"  {level}: {count}")
    print("-" * 30)

def main():
    parser = argparse.ArgumentParser(
        description="Analyze application log files in a directory."
    )
    parser.add_argument(
        "--log-dir",
        required=True,
        help="Directory containing .log files"
    )

    args = parser.parse_args()
    log_dir = Path(args.log_dir)

    try:
        analyzer = LogAnalyzer(log_dir)
        report = analyzer.analyze()
        print_report(report)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
