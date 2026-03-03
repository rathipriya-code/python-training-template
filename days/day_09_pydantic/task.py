"""
Day 09: Pydantic Models and Validation
=======================================

Theme: Consulting Timesheet Tracker - Data Models with Validation

Learning Objectives:
- Create Pydantic models for data validation
- Use Field validators and constraints
- Implement custom validators
- Work with nested models
- Serialize and deserialize data

Business Context:
Build robust data models with automatic validation for API
requests and responses in preparation for FastAPI.
"""

from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List
from datetime import date
from enum import Enum


class ProjectStatus(str, Enum):
    """Project status enumeration"""

    ACTIVE = "active"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ConsultantBase(BaseModel):
    """
    Base Pydantic model for Consultant.

    Fields:
        name: Consultant full name (2-100 characters)
        employee_id: Unique employee ID (format: EMP followed by 3-6 digits)
        hourly_rate: Hourly billing rate (must be positive, max 1000.0)
        email: Email address
    """

    pass


class ConsultantCreate(ConsultantBase):
    """Model for creating a new consultant"""

    pass


class Consultant(ConsultantBase):
    """
    Full consultant model with ID.

    Additional fields:
        id: Auto-generated integer ID

    Config:
        from_attributes = True (allows creating from ORM objects)
    """

    pass


class ProjectBase(BaseModel):
    """
    Base model for Project.

    Fields:
        code: Project code (3-20 chars, uppercase, alphanumeric with dashes)
        client_name: Client name (2-100 characters)
        budget_hours: Total budgeted hours (positive, max 10000.0)
        status: Project status (enum)
    """

    pass


class Project(ProjectBase):
    """
    Full project model.

    Additional fields:
        id: Integer ID
        hours_used: Hours used so far (default 0.0)

    Add a computed property or method:
        remaining_hours: Returns budget_hours - hours_used
    """

    pass


class TimesheetEntryBase(BaseModel):
    """
    Base model for timesheet entry.

    Fields:
        consultant_id: Integer
        project_id: Integer
        hours: Hours worked (0.5 to 24.0)
        entry_date: Date object
        description: Optional description (max 500 chars)

    Validators:
        - hours must be in increments of 0.5 (e.g., 7.5, 8.0, not 7.3)
        - entry_date cannot be in the future
    """

    pass


class TimesheetEntryCreate(TimesheetEntryBase):
    """Model for creating timesheet entry"""

    pass


class TimesheetEntry(TimesheetEntryBase):
    """
    Full timesheet entry with computed fields.

    Additional fields:
        id: Integer ID
        consultant: Optional[Consultant] - nested consultant object
        project: Optional[Project] - nested project object

    Config:
        from_attributes = True
    """

    pass


class TimesheetSummary(BaseModel):
    """
    Summary model for reporting.

    Fields:
        total_entries: int
        total_hours: float
        consultants: List[str] - consultant names
        projects: List[str] - project codes
        date_range: tuple[date, date] - start and end dates
    """

    pass


class BulkTimesheetCreate(BaseModel):
    """
    Model for bulk timesheet creation.

    Fields:
        entries: List of TimesheetEntryCreate objects (min 1, max 100)
        validate_consultants: bool - whether to validate consultant IDs exist
        validate_projects: bool - whether to validate project IDs exist
    """

    pass


def validate_employee_id(value: str) -> str:
    """
    Validate employee ID format: EMP followed by 3-6 digits.

    Args:
        value: Employee ID string

    Returns:
        Validated employee ID

    Raises:
        ValueError: If format is invalid

    Example:
        >>> validate_employee_id("EMP001")
        "EMP001"
        >>> validate_employee_id("ABC123")
        Traceback (most recent call last):
        ...
        ValueError: ...
    """
    pass


def validate_project_code(value: str) -> str:
    """
    Validate and normalize project code.
    Must be 3-20 chars, alphanumeric with dashes, converts to uppercase.

    Args:
        value: Project code

    Returns:
        Normalized project code (uppercase)

    Raises:
        ValueError: If format is invalid

    Example:
        >>> validate_project_code("acm-101")
        "ACM-101"
        >>> validate_project_code("ab")
        Traceback (most recent call last):
        ...
        ValueError: ...
    """
    pass


def create_consultant_from_dict(data: dict) -> Consultant:
    """
    Create a Consultant model from dictionary with validation.

    Args:
        data: Dictionary with consultant data

    Returns:
        Validated Consultant instance

    Raises:
        ValidationError: If data is invalid

    Example:
        >>> data = {
        ...     "id": 1,
        ...     "name": "John Doe",
        ...     "employee_id": "EMP001",
        ...     "hourly_rate": 75.0,
        ...     "email": "john@example.com"
        ... }
        >>> consultant = create_consultant_from_dict(data)
        >>> consultant.name
        "John Doe"
    """
    pass


def serialize_timesheet_entry(entry: TimesheetEntry) -> dict:
    """
    Serialize timesheet entry to dictionary.

    Args:
        entry: TimesheetEntry instance

    Returns:
        Dictionary representation

    Example:
        >>> entry = TimesheetEntry(...)
        >>> data = serialize_timesheet_entry(entry)
        >>> isinstance(data, dict)
        True
    """
    pass


def validate_timesheet_batch(
    entries: List[dict],
) -> tuple[List[TimesheetEntryCreate], List[str]]:
    """
    Validate a batch of timesheet entries.

    Args:
        entries: List of entry dictionaries

    Returns:
        Tuple of (valid_entries, error_messages)

    Example:
        >>> entries = [
        ...     {"consultant_id": 1, "project_id": 1, "hours": 8.0, "entry_date": "2026-02-10"},
        ...     {"consultant_id": 1, "project_id": 1, "hours": 50.0, "entry_date": "2026-02-10"}
        ... ]
        >>> valid, errors = validate_timesheet_batch(entries)
        >>> len(errors) > 0
        True
    """
    pass
