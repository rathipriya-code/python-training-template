"""
Day 04: Error Handling and Exceptions
======================================

Theme: Consulting Timesheet Tracker - Robust Data Validation

Learning Objectives:
- Master try/except blocks for error handling
- Create custom exceptions
- Use else and finally clauses
- Validate user input with appropriate error messages

Business Context:
Build robust validation for timesheet data to prevent
invalid entries and provide clear error messages.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime




class TimesheetValidationError(Exception):
    """Custom exception for timesheet validation errors"""
    pass


class InvalidHoursError(TimesheetValidationError):
    """Raised when hours value is invalid"""
    pass


class InvalidDateError(TimesheetValidationError):
    """Raised when date format is invalid"""
    pass


def validate_hours(hours: float) -> float:
    """
    Validate that hours are within acceptable range (0.5 to 24.0).
    
    Args:
        hours: Number of hours to validate
    
    Returns:
        The validated hours value
    
    Raises:
        InvalidHoursError: If hours are negative, zero, or > 24
        TypeError: If hours is not a number
    
    Example:
        >>> validate_hours(8.0)
        8.0
        >>> validate_hours(-5.0)
        Traceback (most recent call last):
        ...
        InvalidHoursError: Hours must be between 0.5 and 24.0, got -5.0
    """
    if not isinstance(hours, (int, float)):
        raise TypeError(f"Hours must be a number, got {type(hours).__name__}")
    elif hours < 0.5 or hours > 24.0:
        raise InvalidHoursError(f"Hours must be between 0.5 and 24.0, got {hours}")
    return float(hours)
def validate_date(date_str: str) -> datetime:
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise InvalidDateError(f"Invalid date format: {date_str}. Use   YYYY-MM-DD")



def safe_divide_hours(total_hours: float, days: int) -> Optional[float]:
    """
    Safely divide total hours by number of days.
    
    Args:
        total_hours: Total hours to divide
        days: Number of days to divide by
    
    Returns:
        Average hours per day, or None if division by zero
    
    Example:
        >>> safe_divide_hours(40.0, 5)
        8.0
        >>> safe_divide_hours(40.0, 0) is None
        True
    """
    try:
        average = total_hours / days
        return average
    except ZeroDivisionError:
        return None
    except Exception as e:
        print(f"An Unexpected error occurred: {e}")
        return None


def parse_date(date_string: str) -> tuple[int, int, int]:
    """
    Parse a date string in format "YYYY-MM-DD" and validate it.
    
    Args:
        date_string: Date string to parse
    
    Returns:
        Tuple of (year, month, day) as integers
    
    Raises:
        InvalidDateError: If date format is invalid or values are out of range
    
    Example:
        >>> parse_date("2026-02-10")
        (2026, 2, 10)
        >>> parse_date("2026-13-01")
        Traceback (most recent call last):
        ...
        InvalidDateError: Month must be between 1 and 12, got 13
    """
    if not isinstance(date_string, str):
        raise InvalidDateError("Date must be in format YYYY-MM-DD")

    parts = date_string.split("-")

    if len(parts) != 3:
        raise InvalidDateError("Date must be in format YYYY-MM-DD")

    year_str, month_str, day_str = parts
    if not (
        len(year_str) == 4 and
        len(month_str) == 2 and
        len(day_str) == 2 and
        year_str.isdigit() and
        month_str.isdigit() and
        day_str.isdigit()
    ):
        raise InvalidDateError("Date must be in format YYYY-MM-DD")

    year = int(year_str)
    month = int(month_str)
    day = int(day_str)

    if month < 1 or month > 12:
        raise InvalidDateError(f"Month must be between 1 and 12, got {month}")

    if day < 1 or day > 31:
        raise InvalidDateError(f"Day must be between 1 and 31, got {day}")

    return (year, month, day)

def validate_and_create_entry(
    consultant: str,
    project: str,
    hours: float,
    date: str
) -> Dict[str, Any]:
    """
    Validate all fields and create a timesheet entry.
    
    Args:
        consultant: Consultant name (must not be empty)
        project: Project code (must not be empty)
        hours: Hours worked (must be 0.5 to 24.0)
        date: Date in format "YYYY-MM-DD"
    
    Returns:
        Dictionary with validated timesheet entry
    
    Raises:
        TimesheetValidationError: If any validation fails
    
    Example:
        >>> entry = validate_and_create_entry("John Doe", "ACM-101", 8.0, "2026-02-10")
        >>> entry["consultant"]
        "John Doe"
        >>> validate_and_create_entry("", "ACM-101", 8.0, "2026-02-10")
        Traceback (most recent call last):
        ...
        TimesheetValidationError: Consultant name cannot be empty
    """
    if not consultant.strip():
        raise TimesheetValidationError("Consultant name cannot be empty")

    if not project.strip():
        raise TimesheetValidationError("Project code cannot be empty")

    val_hours = validate_hours(hours)

    parse_date(date)  

    return {
        "consultant": consultant.strip(),
        "project": project.strip(),
        "hours": val_hours,
        "date": date
    }



def safe_get_nested_value(
    data: Dict[str, Any],
    *keys: str,
    default: Any = None
) -> Any:
    """
    Safely get a nested value from a dictionary.
    
    Args:
        data: Dictionary to search
        *keys: Variable number of keys to traverse
        default: Default value if key path doesn't exist
    
    Returns:
        The value if found, otherwise default
    
    Example:
        >>> data = {"consultant": {"name": "John", "id": 123}}
        >>> safe_get_nested_value(data, "consultant", "name")
        "John"
        >>> safe_get_nested_value(data, "consultant", "email", default="N/A")
        "N/A"
        >>> safe_get_nested_value(data, "invalid", "path", default="N/A")
        "N/A"
    """
    current = data

    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default

    return current



def process_timesheet_batch(
    entries: List[Dict[str, Any]]
) -> tuple[List[Dict[str, Any]], List[str]]:
    """
    Process a batch of timesheet entries, collecting valid ones and error messages.
    Each entry should have keys: consultant, project, hours, date
    
    Args:
        entries: List of timesheet entry dictionaries to validate
    
    Returns:
        Tuple of (valid_entries, error_messages)
        - valid_entries: List of successfully validated entries
        - error_messages: List of error messages for invalid entries
    
    Example:
        >>> entries = [
        ...     {"consultant": "John", "project": "ACM-101", "hours": 8.0, "date": "2026-02-10"},
        ...     {"consultant": "", "project": "BET-5", "hours": 6.0, "date": "2026-02-11"},
        ...     {"consultant": "Jane", "project": "ZET-99", "hours": 7.0, "date": "2026-02-12"}
        ... ]
        >>> valid, errors = process_timesheet_batch(entries)
        >>> len(valid)
        2
        >>> len(errors)
        1
    """
    valid_entries: List[Dict[str, Any]] = []
    error_messages: List[str] = []
    for index, entry in enumerate(entries, start=1):

        try:
            validated_entry = validate_and_create_entry(
                entry["consultant"],
                entry["project"],
                entry["hours"],
                entry["date"]
            )
            valid_entries.append(validated_entry)

        except Exception as e:
            error_messages.append(
                f"Entry {index}: {str(e)}"
            )

    return valid_entries, error_messages



def calculate_with_fallback(
    hours: float,
    rate: float,
    fallback_rate: float = 50.0
) -> float:
    """
    Calculate billable amount with fallback for invalid rates.
    
    Args:
        hours: Hours worked
        rate: Hourly rate
        fallback_rate: Rate to use if primary rate is invalid
    
    Returns:
        Calculated amount (hours * rate, or hours * fallback_rate if rate <= 0)
    
    Example:
        >>> calculate_with_fallback(8.0, 75.0)
        600.0
        >>> calculate_with_fallback(8.0, 0.0)
        400.0
        >>> calculate_with_fallback(8.0, -10.0, 60.0)
        480.0
    """
    valid_rate = rate if rate > 0 else fallback_rate
    return hours * valid_rate



def guaranteed_cleanup_operation(
    filepath: str,
    data: str
) -> bool:
    """
    Demonstrate try/except/else/finally with a mock file operation.
    
    This function simulates:
    - Writing data (raises ValueError if filepath is empty)
    - Success message in else clause
    - Cleanup in finally clause
    
    Args:
        filepath: Path where data should be written
        data: Data to write
    
    Returns:
        True if successful, False if an error occurred
    
    Note:
        This is a mock function for demonstrating exception handling patterns.
        It doesn't actually write to a file.
    
    Example:
        >>> guaranteed_cleanup_operation("timesheet.txt", "data")
        True
        >>> guaranteed_cleanup_operation("", "data")
        False
    """

    try:
        if not filepath.strip():
            raise ValueError("Filepath cannot be empty")

        print(f"Writing data to {filepath}...")
    
    except Exception:
        return False

    else:
        print("Write operation successful.")
        return True

    finally:
        print("Cleanup completed.")


