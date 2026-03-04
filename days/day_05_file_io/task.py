"""
Day 05: File I/O Operations
============================

Theme: Consulting Timesheet Tracker - Data Persistence

Learning Objectives:
- Read and write text files
- Work with CSV files
- Handle JSON data
- Implement proper file handling with context managers

Business Context:
Import/export timesheet data from various file formats,
enabling integration with other systems and data backup.
"""

import json
import csv
from typing import List, Dict, Any
from pathlib import Path


def write_timesheets_to_json(timesheets: List[Dict[str, Any]], filepath: str) -> None:
    """
    Write timesheets to a JSON file.

    Args:
        timesheets: List of timesheet dictionaries
        filepath: Path where JSON file should be written

    Example:
        >>> timesheets = [{"consultant": "John", "hours": 8.0}]
        >>> write_timesheets_to_json(timesheets, "timesheets.json")
    """
    path = Path(filepath)

    with path.open("w", encoding="utf-8") as f:
        json.dump(timesheets, f, indent=4)


def read_timesheets_from_json(filepath: str) -> List[Dict[str, Any]]:
    """
    Read timesheets from a JSON file.

    Args:
        filepath: Path to JSON file

    Returns:
        List of timesheet dictionaries

    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If file contains invalid JSON

    Example:
        >>> timesheets = read_timesheets_from_json("timesheets.json")
        >>> len(timesheets) > 0
        True
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"{filepath} not found")
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("JSON must contain a list of timesheets")

    return data


def write_timesheets_to_csv(timesheets: List[Dict[str, Any]], filepath: str) -> None:
    """
    Write timesheets to a CSV file.
    CSV headers: consultant, project, hours, date

    Args:
        timesheets: List of timesheet dictionaries
        filepath: Path where CSV file should be written

    Example:
        >>> timesheets = [
        ...     {"consultant": "John", "project": "ACM-101", "hours": 8.0, "date": "2026-02-10"}
        ... ]
        >>> write_timesheets_to_csv(timesheets, "timesheets.csv")
    """
    path = Path(filepath)
    fieldnames = ["consultant", "project", "hours", "date"]

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(timesheets)


def read_timesheets_from_csv(filepath: str) -> List[Dict[str, Any]]:
    """
    Read timesheets from a CSV file.
    Expected headers: consultant, project, hours, date
    Convert hours to float.

    Args:
        filepath: Path to CSV file

    Returns:
        List of timesheet dictionaries

    Raises:
        FileNotFoundError: If file doesn't exist

    Example:
        >>> timesheets = read_timesheets_from_csv("timesheets.csv")
        >>> isinstance(timesheets[0]["hours"], float)
        True
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"{filepath} not found")

    timesheets: List[Dict[str, Any]] = []

    with path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            row["hours"] = float(row["hours"])
            timesheets.append(row)

    return timesheets


def append_timesheet_to_csv(entry: Dict[str, Any], filepath: str) -> None:
    """
    Append a single timesheet entry to an existing CSV file.
    If file doesn't exist, create it with headers.

    Args:
        entry: Single timesheet dictionary
        filepath: Path to CSV file

    Example:
        >>> entry = {"consultant": "Jane", "project": "BET-5", "hours": 7.0, "date": "2026-02-11"}
        >>> append_timesheet_to_csv(entry, "timesheets.csv")
    """
    path = Path(filepath)
    fieldnames = ["consultant", "project", "hours", "date"]

    file_exists = path.exists()

    with path.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()

        writer.writerow(entry)


def generate_summary_report(timesheets: List[Dict[str, Any]], output_file: str) -> None:
    """
    Generate a text summary report of timesheets.

    Format:
    TIMESHEET SUMMARY REPORT
    ========================
    Total Entries: X
    Total Hours: Y

    By Consultant:
    - Consultant Name: Z hours
    ...

    Args:
        timesheets: List of timesheet dictionaries
        output_file: Path where report should be written

    Example:
        >>> timesheets = [
        ...     {"consultant": "John", "hours": 8.0},
        ...     {"consultant": "John", "hours": 7.0}
        ... ]
        >>> generate_summary_report(timesheets, "report.txt")
    """
    total_entries = len(timesheets)
    total_hours = float(sum(entry.get("hours", 0.0) for entry in timesheets))

    consultant_totals: Dict[str, float] = {}

    for entry in timesheets:
        consultant = entry.get("consultant", "Unknown")
        hours = entry.get("hours", 0.0)
        consultant_totals[consultant] = consultant_totals.get(consultant, 0.0) + hours

    path = Path(output_file)

    with path.open("w", encoding="utf-8") as f:
        f.write("TIMESHEET SUMMARY REPORT\n")
        f.write("========================\n")
        f.write(f"Total Entries: {total_entries}\n")
        f.write(f"Total Hours: {total_hours}\n\n")

        f.write("By Consultant:\n")
        for consultant, hours in sorted(consultant_totals.items()):
            f.write(f"- {consultant}: {hours} hours\n")


def read_configuration(filepath: str) -> Dict[str, Any]:
    """
    Read configuration from a JSON file with default values.

    Default configuration:
    {
        "standard_hours": 40.0,
        "overtime_multiplier": 1.5,
        "billable_rate": 75.0
    }

    Args:
        filepath: Path to configuration JSON file

    Returns:
        Configuration dictionary (defaults if file doesn't exist)

    Example:
        >>> config = read_configuration("config.json")
        >>> "standard_hours" in config
        True
    """

    default_config = {
        "standard_hours": 40.0,
        "overtime_multiplier": 1.5,
        "billable_rate": 75.0,
    }

    path = Path(filepath)
    if not path.exists():
        return default_config

    try:
        with path.open("r", encoding="utf-8") as f:
            config = json.load(f)
        if isinstance(config, dict):
            return {**default_config, **config}
        return default_config

    except json.JSONDecodeError:
        return default_config


def backup_timesheets(source_file: str, backup_dir: str, backup_name: str) -> str:
    """
    Create a backup copy of a timesheet file.

    Args:
        source_file: Path to source file
        backup_dir: Directory where backup should be stored
        backup_name: Name for backup file

    Returns:
        Full path to created backup file

    Raises:
        FileNotFoundError: If source file doesn't exist

    Example:
        >>> backup_path = backup_timesheets("timesheets.json", "backups", "timesheets_backup.json")
        >>> Path(backup_path).exists()
        True
    """
    source_path = Path(source_file)
    if not source_path.exists():
        raise FileNotFoundError(f"{source_file} not found")
    backup_directory = Path(backup_dir)
    backup_directory.mkdir(parents=True, exist_ok=True)
    backup_path = backup_directory / backup_name
    backup_path.write_bytes(source_path.read_bytes())

    return str(backup_path)


def merge_json_files(file_paths: List[str], output_file: str) -> int:
    """
    Merge multiple JSON timesheet files into one.

    Args:
        file_paths: List of paths to JSON files to merge
        output_file: Path where merged file should be written

    Returns:
        Total number of entries in merged file

    Note:
        Silently skip files that don't exist or contain invalid JSON

    Example:
        >>> count = merge_json_files(["file1.json", "file2.json"], "merged.json")
        >>> count >= 0
        True
    """
    merged_data: List[Dict[str, Any]] = []

    for file_path in file_paths:
        path = Path(file_path)
        if not path.exists():
            continue

        try:
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    merged_data.extend(data)
        except json.JSONDecodeError:
            continue
    output_path = Path(output_file)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(merged_data, f, indent=4)

    return len(merged_data)


def export_consultant_hours(
    timesheets: List[Dict[str, Any]], consultant_name: str, output_file: str
) -> None:
    """
    Export hours for a specific consultant to a text file.

    Format (one line per entry):
    YYYY-MM-DD | PROJECT-CODE | X.X hours

    Args:
        timesheets: List of timesheet dictionaries
        consultant_name: Name of consultant to export
        output_file: Path where export should be written

    Example:
        >>> timesheets = [
        ...     {"consultant": "John", "project": "ACM-101", "hours": 8.0, "date": "2026-02-10"}
        ... ]
        >>> export_consultant_hours(timesheets, "John", "john_hours.txt")
    """
    path = Path(output_file)

    with path.open("w", encoding="utf-8") as f:
        for entry in timesheets:
            if entry.get("consultant") == consultant_name:
                date = entry.get("date", "")
                project = entry.get("project", "")
                hours = entry.get("hours", 0.0)
                f.write(f"{date} | {project} | {hours} hours\n")
