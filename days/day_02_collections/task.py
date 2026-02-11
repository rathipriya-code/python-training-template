"""
Day 02: Lists and Dictionaries
===============================

Theme: Consulting Timesheet Tracker - Working with Collections

Learning Objectives:
- Master list operations (append, extend, slicing)
- Work with dictionaries (keys, values, items)
- Understand mutable vs immutable data structures
- Combine lists and dictionaries for real-world data

Business Context:
Today you'll work with collections of timesheet entries, managing
multiple consultants and their logged hours across different projects.
"""

from typing import List, Dict, Any, Optional


def add_timesheet_entry(
    timesheets: List[Dict[str, Any]],
    consultant: str,
    project: str,
    hours: float,
    date: str
) -> List[Dict[str, Any]]:
    """
    Add a new timesheet entry to the list of timesheets.
    
    Args:
        timesheets: Existing list of timesheet dictionaries
        consultant: Name of the consultant
        project: Project code
        hours: Hours worked
        date: Date in format "YYYY-MM-DD"
    
    Returns:
        Updated list of timesheets with the new entry added
    
    Example:
        >>> timesheets = []
        >>> result = add_timesheet_entry(timesheets, "John Doe", "ACM-101", 8.0, "2026-02-10")
        >>> len(result)
        1
        >>> result[0]["consultant"]
        "John Doe"
    """
    pass


def get_total_hours_by_consultant(
    timesheets: List[Dict[str, Any]],
    consultant: str
) -> float:
    """
    Calculate the total hours logged by a specific consultant.
    
    Args:
        timesheets: List of timesheet dictionaries
        consultant: Name of the consultant to filter by
    
    Returns:
        Total hours worked by the consultant
    
    Example:
        >>> timesheets = [
        ...     {"consultant": "John Doe", "hours": 8.0},
        ...     {"consultant": "Jane Smith", "hours": 6.0},
        ...     {"consultant": "John Doe", "hours": 7.5}
        ... ]
        >>> get_total_hours_by_consultant(timesheets, "John Doe")
        15.5
    """
    pass


def get_projects_for_consultant(
    timesheets: List[Dict[str, Any]],
    consultant: str
) -> List[str]:
    """
    Get a unique list of projects a consultant has worked on.
    The list should be sorted alphabetically and contain no duplicates.
    
    Args:
        timesheets: List of timesheet dictionaries
        consultant: Name of the consultant
    
    Returns:
        Sorted list of unique project codes
    
    Example:
        >>> timesheets = [
        ...     {"consultant": "John Doe", "project": "ACM-101"},
        ...     {"consultant": "John Doe", "project": "BET-5"},
        ...     {"consultant": "John Doe", "project": "ACM-101"}
        ... ]
        >>> get_projects_for_consultant(timesheets, "John Doe")
        ["ACM-101", "BET-5"]
    """
    pass


def create_consultant_summary(timesheets: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Create a summary dictionary mapping consultant names to their total hours.
    
    Args:
        timesheets: List of timesheet dictionaries (must have 'consultant' and 'hours' keys)
    
    Returns:
        Dictionary with consultant names as keys and total hours as values
    
    Example:
        >>> timesheets = [
        ...     {"consultant": "John Doe", "hours": 8.0},
        ...     {"consultant": "Jane Smith", "hours": 6.0},
        ...     {"consultant": "John Doe", "hours": 7.5}
        ... ]
        >>> create_consultant_summary(timesheets)
        {"John Doe": 15.5, "Jane Smith": 6.0}
    """
    pass


def get_entries_by_date_range(
    timesheets: List[Dict[str, Any]],
    start_date: str,
    end_date: str
) -> List[Dict[str, Any]]:
    """
    Filter timesheets to only include entries within a date range (inclusive).
    Dates are in format "YYYY-MM-DD" and can be compared as strings.
    
    Args:
        timesheets: List of timesheet dictionaries
        start_date: Start date (inclusive)
        end_date: End date (inclusive)
    
    Returns:
        List of timesheet entries within the date range
    
    Example:
        >>> timesheets = [
        ...     {"date": "2026-02-01", "hours": 8.0},
        ...     {"date": "2026-02-15", "hours": 7.0},
        ...     {"date": "2026-02-28", "hours": 6.0}
        ... ]
        >>> result = get_entries_by_date_range(timesheets, "2026-02-10", "2026-02-20")
        >>> len(result)
        1
        >>> result[0]["date"]
        "2026-02-15"
    """
    pass


def merge_timesheet_lists(
    list1: List[Dict[str, Any]],
    list2: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Merge two timesheet lists without modifying the original lists.
    
    Args:
        list1: First list of timesheets
        list2: Second list of timesheets
    
    Returns:
        New list containing all entries from both lists
    
    Example:
        >>> list1 = [{"id": 1, "hours": 8}]
        >>> list2 = [{"id": 2, "hours": 6}]
        >>> result = merge_timesheet_lists(list1, list2)
        >>> len(result)
        2
        >>> len(list1)  # Original list unchanged
        1
    """
    pass


def update_project_code(
    timesheets: List[Dict[str, Any]],
    old_code: str,
    new_code: str
) -> List[Dict[str, Any]]:
    """
    Update all entries with old project code to use new project code.
    Modifies the timesheets in place and returns the updated list.
    
    Args:
        timesheets: List of timesheet dictionaries
        old_code: Old project code to replace
        new_code: New project code to use
    
    Returns:
        The modified timesheets list
    
    Example:
        >>> timesheets = [
        ...     {"project": "ACM-101", "hours": 8},
        ...     {"project": "BET-5", "hours": 6},
        ...     {"project": "ACM-101", "hours": 7}
        ... ]
        >>> update_project_code(timesheets, "ACM-101", "ACM-102")
        >>> timesheets[0]["project"]
        "ACM-102"
    """
    pass
