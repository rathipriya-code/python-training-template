"""
Day 03: Comprehensions
======================

Theme: Consulting Timesheet Tracker - Data Transformation

Learning Objectives:
- Master list comprehensions for transforming data
- Use dictionary comprehensions for data aggregation
- Apply filtering with comprehensions
- Understand nested comprehensions for complex data

Business Context:
Transform and filter timesheet data efficiently using Pythonic
comprehensions to generate reports and insights.
"""

from typing import List, Dict, Any, Set


def extract_consultant_names(timesheets: List[Dict[str, Any]]) -> List[str]:
    """
    Extract all consultant names from timesheets using list comprehension.

    Args:
        timesheets: List of timesheet dictionaries

    Returns:
        List of consultant names (may contain duplicates)

    Example:
        >>> timesheets = [
        ...     {"consultant": "John Doe", "hours": 8},
        ...     {"consultant": "Jane Smith", "hours": 6}
        ... ]
        >>> extract_consultant_names(timesheets)
        ["John Doe", "Jane Smith"]
    """
    pass


def get_high_hour_entries(
    timesheets: List[Dict[str, Any]], threshold: float
) -> List[Dict[str, Any]]:
    """
    Filter timesheets to only include entries with hours >= threshold.
    Use list comprehension.

    Args:
        timesheets: List of timesheet dictionaries
        threshold: Minimum hours to include

    Returns:
        Filtered list of high-hour entries

    Example:
        >>> timesheets = [
        ...     {"consultant": "John", "hours": 8.0},
        ...     {"consultant": "Jane", "hours": 4.0},
        ...     {"consultant": "Bob", "hours": 10.0}
        ... ]
        >>> result = get_high_hour_entries(timesheets, 7.0)
        >>> len(result)
        2
    """
    pass


def calculate_daily_totals(timesheets: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Create a dictionary mapping dates to total hours worked that day.
    Use dictionary comprehension.

    Args:
        timesheets: List of timesheet dictionaries with 'date' and 'hours' keys

    Returns:
        Dictionary with dates as keys and total hours as values

    Example:
        >>> timesheets = [
        ...     {"date": "2026-02-10", "hours": 8.0},
        ...     {"date": "2026-02-10", "hours": 6.0},
        ...     {"date": "2026-02-11", "hours": 7.0}
        ... ]
        >>> calculate_daily_totals(timesheets)
        {"2026-02-10": 14.0, "2026-02-11": 7.0}
    """
    pass


def get_billable_hours_map(
    timesheets: List[Dict[str, Any]], billable_rate: float
) -> Dict[str, float]:
    """
    Create a dictionary mapping consultant names to their billable hours.
    Calculate billable hours as: hours * billable_rate / 100
    Use dictionary comprehension with aggregation.

    Args:
        timesheets: List of timesheet dictionaries with 'consultant' and 'hours'
        billable_rate: Percentage of hours that are billable (0-100)

    Returns:
        Dictionary mapping consultant names to total billable hours

    Example:
        >>> timesheets = [
        ...     {"consultant": "John", "hours": 40.0},
        ...     {"consultant": "Jane", "hours": 30.0},
        ...     {"consultant": "John", "hours": 10.0}
        ... ]
        >>> get_billable_hours_map(timesheets, 80.0)
        {"John": 40.0, "Jane": 24.0}
    """
    pass


def extract_unique_projects(timesheets: List[Dict[str, Any]]) -> Set[str]:
    """
    Extract unique project codes using set comprehension.

    Args:
        timesheets: List of timesheet dictionaries with 'project' key

    Returns:
        Set of unique project codes

    Example:
        >>> timesheets = [
        ...     {"project": "ACM-101"},
        ...     {"project": "BET-5"},
        ...     {"project": "ACM-101"}
        ... ]
        >>> extract_unique_projects(timesheets)
        {"ACM-101", "BET-5"}
    """
    pass


def create_consultant_project_matrix(
    timesheets: List[Dict[str, Any]],
) -> Dict[str, List[str]]:
    """
    Create a dictionary mapping each consultant to their list of unique projects.
    Use nested comprehensions.

    Args:
        timesheets: List of timesheet dictionaries

    Returns:
        Dictionary with consultant names as keys and lists of unique projects as values
        Projects should be sorted alphabetically

    Example:
        >>> timesheets = [
        ...     {"consultant": "John", "project": "ACM-101"},
        ...     {"consultant": "John", "project": "BET-5"},
        ...     {"consultant": "Jane", "project": "ACM-101"}
        ... ]
        >>> create_consultant_project_matrix(timesheets)
        {"John": ["ACM-101", "BET-5"], "Jane": ["ACM-101"]}
    """
    pass


def transform_to_uppercase_projects(
    timesheets: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Create a new list where all project codes are converted to uppercase.
    Use list comprehension with dictionary manipulation.

    Args:
        timesheets: List of timesheet dictionaries

    Returns:
        New list with uppercase project codes

    Example:
        >>> timesheets = [
        ...     {"consultant": "John", "project": "acm-101", "hours": 8},
        ...     {"consultant": "Jane", "project": "bet-5", "hours": 6}
        ... ]
        >>> result = transform_to_uppercase_projects(timesheets)
        >>> result[0]["project"]
        "ACM-101"
    """
    pass


def filter_and_transform(
    timesheets: List[Dict[str, Any]], min_hours: float, project_prefix: str
) -> List[str]:
    """
    Filter entries by minimum hours AND project prefix, then return consultant names.
    Use list comprehension with multiple conditions.

    Args:
        timesheets: List of timesheet dictionaries
        min_hours: Minimum hours threshold
        project_prefix: Required project code prefix (e.g., "ACM")

    Returns:
        List of consultant names meeting both criteria

    Example:
        >>> timesheets = [
        ...     {"consultant": "John", "project": "ACM-101", "hours": 8},
        ...     {"consultant": "Jane", "project": "BET-5", "hours": 9},
        ...     {"consultant": "Bob", "project": "ACM-102", "hours": 6}
        ... ]
        >>> filter_and_transform(timesheets, 7.0, "ACM")
        ["John"]
    """
    pass


def nested_hours_by_consultant_and_project(
    timesheets: List[Dict[str, Any]],
) -> Dict[str, Dict[str, float]]:
    """
    Create a nested dictionary: consultant -> project -> total hours.
    Use nested dictionary comprehension.

    Args:
        timesheets: List of timesheet dictionaries

    Returns:
        Nested dictionary with consultant names as outer keys,
        project codes as inner keys, and total hours as values

    Example:
        >>> timesheets = [
        ...     {"consultant": "John", "project": "ACM-101", "hours": 8},
        ...     {"consultant": "John", "project": "ACM-101", "hours": 7},
        ...     {"consultant": "John", "project": "BET-5", "hours": 6}
        ... ]
        >>> result = nested_hours_by_consultant_and_project(timesheets)
        >>> result["John"]["ACM-101"]
        15.0
        >>> result["John"]["BET-5"]
        6.0
    """
    pass
