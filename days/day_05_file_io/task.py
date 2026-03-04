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

from typing import List, Dict, Any


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
    pass


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
    pass


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
    pass


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
    pass


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
    pass


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
    pass


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
    pass


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
    pass


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
    pass


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
    pass
