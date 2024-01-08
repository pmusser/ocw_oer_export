"""
Command-line interface (CLI) for the OCW OER Export Project.

This module provides a CLI to generate JSON or CSV files containing
MIT OpenCourseWare courses' metadata.
"""
import argparse
from .create_csv import create_csv
from .create_json import create_json


def main():
    """
    Parses command-line arguments and executes the appropriate function.
    """
    parser = argparse.ArgumentParser(description="OCW OER Export")

    parser.add_argument("--create_csv", action="store_true", help="Create CSV file")
    parser.add_argument("--create_json", action="store_true", help="Create JSON file")
    parser.add_argument(
        "--source",
        choices=["api", "json"],
        default="api",
        help="Specify data source for CSV creation (default: api)",
    )

    args = parser.parse_args()

    if args.create_csv:
        create_csv(source=args.source)
    elif args.create_json:
        create_json()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
