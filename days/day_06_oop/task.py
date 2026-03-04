"""
Day 06: Object-Oriented Programming
====================================

Theme: Consulting Timesheet Tracker - Data Models

Learning Objectives:
- Create classes with proper initialization
- Implement instance and class methods
- Use properties and private attributes
- Understand inheritance and composition

Business Context:
Build robust object-oriented models for consultants,
projects, and timesheet entries with proper encapsulation.
"""

from typing import List


class Consultant:
    """Represents a consultant in the timesheet system"""

    def __init__(self, name: str, employee_id: str, hourly_rate: float):
        """
        Initialize a Consultant.

        Args:
            name: Full name of the consultant
            employee_id: Unique employee identifier
            hourly_rate: Hourly billing rate
        """
        pass

    def calculate_earnings(self, hours: float) -> float:
        """
        Calculate earnings for given hours.

        Args:
            hours: Number of hours worked

        Returns:
            Total earnings (hours * hourly_rate)
        """
        pass

    def get_display_name(self) -> str:
        """
        Get formatted display name.

        Returns:
            Name with employee ID: "Name (ID: employee_id)"
        """
        pass

    def __str__(self) -> str:
        """String representation of consultant"""
        pass

    def __repr__(self) -> str:
        """Developer-friendly representation"""
        pass


class Project:
    """Represents a project in the timesheet system"""

    def __init__(self, code: str, client_name: str, budget_hours: float):
        """
        Initialize a Project.

        Args:
            code: Unique project code
            client_name: Name of the client
            budget_hours: Total budgeted hours for the project
        """
        pass

    def is_over_budget(self, hours_used: float) -> bool:
        """
        Check if project is over budget.

        Args:
            hours_used: Hours already used

        Returns:
            True if over budget, False otherwise
        """
        pass

    def remaining_hours(self, hours_used: float) -> float:
        """
        Calculate remaining hours in budget.

        Args:
            hours_used: Hours already used

        Returns:
            Remaining hours (can be negative if over budget)
        """
        pass

    def __str__(self) -> str:
        """String representation of project"""
        pass


class TimesheetEntry:
    """Represents a single timesheet entry"""

    def __init__(
        self,
        consultant: Consultant,
        project: Project,
        hours: float,
        entry_date: str,
        description: str = "",
    ):
        """
        Initialize a TimesheetEntry.

        Args:
            consultant: Consultant who worked
            project: Project worked on
            hours: Hours worked
            entry_date: Date of work (YYYY-MM-DD)
            description: Optional description of work done
        """
        pass

    def calculate_value(self) -> float:
        """
        Calculate the monetary value of this entry.

        Returns:
            Value (hours * consultant hourly rate)
        """
        pass

    def get_summary(self) -> str:
        """
        Get a summary string of the entry.

        Returns:
            Summary: "YYYY-MM-DD: Consultant Name on Project Code (X hours)"
        """
        pass

    def is_overtime(self, threshold: float = 8.0) -> bool:
        """
        Check if this entry represents overtime.

        Args:
            threshold: Hours threshold for overtime

        Returns:
            True if hours >= threshold
        """
        pass


class TimesheetManager:
    """Manages a collection of timesheet entries"""

    def __init__(self):
        """Initialize an empty timesheet manager"""
        pass

    def add_entry(self, entry: TimesheetEntry) -> None:
        """
        Add a timesheet entry.

        Args:
            entry: TimesheetEntry to add
        """
        pass

    def get_entries_by_consultant(self, consultant_name: str) -> List[TimesheetEntry]:
        """
        Get all entries for a specific consultant.

        Args:
            consultant_name: Name of consultant

        Returns:
            List of timesheet entries
        """
        pass

    def get_entries_by_project(self, project_code: str) -> List[TimesheetEntry]:
        """
        Get all entries for a specific project.

        Args:
            project_code: Project code

        Returns:
            List of timesheet entries
        """
        pass

    def get_total_hours(self) -> float:
        """
        Calculate total hours across all entries.

        Returns:
            Total hours
        """
        pass

    def get_total_value(self) -> float:
        """
        Calculate total monetary value of all entries.

        Returns:
            Total value
        """
        pass

    def get_consultant_summary(self) -> dict[str, float]:
        """
        Get summary of hours by consultant.

        Returns:
            Dictionary mapping consultant names to total hours
        """
        pass


class BillableProject(Project):
    """A project with billable and non-billable hour tracking"""

    def __init__(
        self, code: str, client_name: str, budget_hours: float, billable_rate: float
    ):
        """
        Initialize a BillableProject.

        Args:
            code: Unique project code
            client_name: Name of the client
            budget_hours: Total budgeted hours
            billable_rate: Percentage of hours that are billable (0-100)
        """
        pass

    def calculate_billable_hours(self, total_hours: float) -> float:
        """
        Calculate billable hours from total hours.

        Args:
            total_hours: Total hours worked

        Returns:
            Billable hours (total_hours * billable_rate / 100)
        """
        pass

    def calculate_billable_amount(
        self, total_hours: float, hourly_rate: float
    ) -> float:
        """
        Calculate total billable amount.

        Args:
            total_hours: Total hours worked
            hourly_rate: Rate per hour

        Returns:
            Billable amount
        """
        pass
