"""
Day 01: Type Hinting and Basic Functions
=========================================

Theme: Consulting Timesheet Tracker - Basic Data Types

Learning Objectives:
- Master Python type hints for functions
- Understand basic data types (str, int, float, bool)
- Work with function parameters and return types
- Introduction to consulting timesheet concepts

Business Context:
You're building a timesheet system for consultants. Today you'll create
basic functions to handle consultant information and time calculations.
"""

from typing import Optional


def calculate_billable_hours(hours_worked: float, billable_percentage: float) -> float:
    """
    Calculate the billable hours based on total hours worked and billable percentage.
    
    Args:
        hours_worked: Total hours worked by the consultant
        billable_percentage: Percentage of time that is billable (0-100)
    
    Returns:
        The number of billable hours (rounded to 2 decimal places)
    
    Example:
        >>> calculate_billable_hours(40.0, 75.0)
        30.0
        >>> calculate_billable_hours(35.5, 50.0)
        17.75
    """
    pass


def format_consultant_name(first_name: str, last_name: str, include_title: bool = False) -> str:
    """
    Format a consultant's name for display in the timesheet system.
    
    Args:
        first_name: Consultant's first name
        last_name: Consultant's last name
        include_title: If True, prepend "Consultant " to the name
    
    Returns:
        Formatted name string
    
    Example:
        >>> format_consultant_name("John", "Doe")
        "John Doe"
        >>> format_consultant_name("Jane", "Smith", True)
        "Consultant Jane Smith"
    """
    pass


def calculate_hourly_rate(annual_salary: int, working_hours_per_week: int = 40) -> float:
    """
    Calculate the hourly rate from an annual salary.
    Assume 52 working weeks per year.
    
    Args:
        annual_salary: Annual salary in dollars
        working_hours_per_week: Number of working hours per week (default: 40)
    
    Returns:
        Hourly rate rounded to 2 decimal places
    
    Example:
        >>> calculate_hourly_rate(104000, 40)
        50.0
        >>> calculate_hourly_rate(78000, 40)
        37.5
    """
    pass


def is_overtime(hours_worked: float, standard_hours: float = 40.0) -> bool:
    """
    Check if the consultant has worked overtime.
    
    Args:
        hours_worked: Number of hours worked in the week
        standard_hours: Standard weekly hours (default: 40.0)
    
    Returns:
        True if overtime was worked, False otherwise
    
    Example:
        >>> is_overtime(45.0)
        True
        >>> is_overtime(40.0)
        False
        >>> is_overtime(38.5)
        False
    """
    pass


def get_project_code(client_name: str, project_id: Optional[int] = None) -> str:
    """
    Generate a project code for timesheet entries.
    Format: First 3 letters of client name (uppercase) + project_id (if provided)
    
    Args:
        client_name: Name of the client
        project_id: Optional project identifier
    
    Returns:
        Generated project code
    
    Example:
        >>> get_project_code("Acme Corp", 101)
        "ACM-101"
        >>> get_project_code("Beta Industries")
        "BET"
        >>> get_project_code("XY", 5)
        "XY-5"
    """
    pass
