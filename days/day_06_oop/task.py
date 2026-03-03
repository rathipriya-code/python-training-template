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

from typing import List, Optional
from datetime import date


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
        self.name = name
        self.employee_id = employee_id
        self.hourly_rate = hourly_rate
    
    def calculate_earnings(self, hours: float) -> float:
        """
        Calculate earnings for given hours.
        
        Args:
            hours: Number of hours worked
        
        Returns:
            Total earnings (hours * hourly_rate)
        """
        total_earnings = hours * self.hourly_rate
        return total_earnings
    
    def get_display_name(self) -> str:
        """
        Get formatted display name.
        
        Returns:
            Name with employee ID: "Name (ID: employee_id)"
        """
        return f"{self.name} (ID: {self.employee_id})"
    
    def __str__(self) -> str:
        """String representation of consultant"""
        return f"consultant {self.get_display_name()}, Hourly Rate:{self.hourly_rate}"
    
    def __repr__(self) -> str:
        """Developer-friendly representation"""
        return (f"Consultant Name: '{self.name}',"
        f"Employee ID: '{self.employee_id}',"
        f"Hourly Rate: '{self.hourly_rate}'"
        )


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
        self.code = code
        self.client_name = client_name
        self.budget_hours = budget_hours
    
    def is_over_budget(self, hours_used: float) -> bool:
        """
        Check if project is over budget.
        
        Args:
            hours_used: Hours already used
        
        Returns:
            True if over budget, False otherwise
        """
        return hours_used > self.budget_hours

    
    def remaining_hours(self, hours_used: float) -> float:
        """
        Calculate remaining hours in budget.
        
        Args:
            hours_used: Hours already used
        
        Returns:
            Remaining hours (can be negative if over budget)
        """
        return self.budget_hours - hours_used
    
    def __str__(self) -> str:
        """String representation of project"""
        return ( f"Project_code: {self.code},"
                f"Client_Name: {self.client_name},"
                f"Budget_hours: {self.budget_hours}")


class TimesheetEntry:
    """Represents a single timesheet entry"""
    
    def __init__(
        self,
        consultant: Consultant,
        project: Project,
        hours: float,
        entry_date: str,
        description: str = ""
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
        self.consultant = consultant
        self.project = project
        self.hours = hours
        self.entry_date = entry_date
        self.description = description
    
    def calculate_value(self) -> float:
        """
        Calculate the monetary value of this entry.
        
        Returns:
            Value (hours * consultant hourly rate)
        """
        return self.hours * self.consultant.hourly_rate
    
    def get_summary(self) -> str:
        """
        Get a summary string of the entry.
        
        Returns:
            Summary: "YYYY-MM-DD: Consultant Name on Project Code (X hours)"
        """
        return(f"Summary: {self.entry_date}: {self.consultant.name} on " f"{self.project.code}" f"({self.hours} hours)")
    
    def is_overtime(self, threshold: float = 8.0) -> bool:
        """
        Check if this entry represents overtime.
        
        Args:
            threshold: Hours threshold for overtime
        
        Returns:
            True if hours >= threshold
        """
        return self.hours >= threshold


class TimesheetManager:
    """Manages a collection of timesheet entries"""
    
    def __init__(self):
        """Initialize an empty timesheet manager"""
        
        self.entries: List[TimesheetEntry] = []
    def add_entry(self, entry: TimesheetEntry) -> None:
        """
        Add a timesheet entry.
        
        Args:
            entry: TimesheetEntry to add
        """
        self.entries.append(entry)
    
    def get_entries_by_consultant(self, consultant_name: str) -> List[TimesheetEntry]:
        """
        Get all entries for a specific consultant.
        
        Args:
            consultant_name: Name of consultant
        
        Returns:
            List of timesheet entries
        """
        return [
            entry for entry in self.entries
            if entry.consultant.name == consultant_name
        ]
    
    
    def get_entries_by_project(self, project_code: str) -> List[TimesheetEntry]:
        """
        Get all entries for a specific project.
        
        Args:
            project_code: Project code
        
        Returns:
            List of timesheet entries
        """
        return [
            entry for entry in self.entries
            if entry.project.code == project_code
        ]
    
    
    def get_total_hours(self) -> float:
        """
        Calculate total hours across all entries.
        
        Returns:
            Total hours
        """
        return sum(entry.hours for entry in self.entries)
    
    
    def get_total_value(self) -> float:
        """
        Calculate total monetary value of all entries.
        
        Returns:
            Total value
        """
        return sum(entry.calculate_value() for entry in self.entries)
    
    
    def get_consultant_summary(self) -> dict[str, float]:
        """
        Get summary of hours by consultant.
        
        Returns:
            Dictionary mapping consultant names to total hours
        """
        summary: dict[str, float] = {}
        
        for entry in self.entries:
            name = entry.consultant.name
            
            if name not in summary:
                summary[name] = 0.0
            
            summary[name] += entry.hours
        
        return summary


class BillableProject(Project):
    """A project with billable and non-billable hour tracking"""
    
    def __init__(
        self,
        code: str,
        client_name: str,
        budget_hours: float,
        billable_rate: float
    ):
        """
        Initialize a BillableProject.
        
        Args:
            code: Unique project code
            client_name: Name of the client
            budget_hours: Total budgeted hours
            billable_rate: Percentage of hours that are billable (0-100)
        """
        self.code = code
        self.client_name = client_name
        self.budget_hours = budget_hours
        self.billable_rate = billable_rate
        if not 0 <= billable_rate <= 100:
            raise ValueError("billable_rate must be between 0 and 100")
     

    
    def calculate_billable_hours(self, total_hours: float) -> float:
        """
        Calculate billable hours from total hours.
        
        Args:
            total_hours: Total hours worked
        
        Returns:
            Billable hours (total_hours * billable_rate / 100)
        """
        return total_hours * (self.billable_rate / 100)
    
    def calculate_billable_amount(
        self,
        total_hours: float,
        hourly_rate: float
    ) -> float:
        """
        Calculate total billable amount.
        
        Args:
            total_hours: Total hours worked
            hourly_rate: Rate per hour
        
        Returns:
            Billable amount
        """
        billable_hours = self.calculate_billable_hours(total_hours)
        return billable_hours * hourly_rate
