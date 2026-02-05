import argparse
from pathlib import Path
from analyzer import LogAnalyzer


def print_report(report: dict):
    """
    Print the analysis summary in the format specified by the assignment.
    """
    print("Log Summary")
    print("-----------")

    # Print log level counts in required order
    for level in ["INFO", "WARNING", "ERROR"]:
        print(f"{level}: {report['level_counts'].get(level, 0)}")

    # Print time range
    print("Time Range:")
    if report["time_range"]:
        start, end = report["time_range"]
        print(f"Start: {start}")
        print(f"End: {end}")
    else:
        print("Start: N/A")
        print("End: N/A")


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


