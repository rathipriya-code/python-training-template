"""
Tests for Day 06: Object-Oriented Programming
"""

import pytest
from .task import (
    Consultant,
    Project,
    TimesheetEntry,
    TimesheetManager,
    BillableProject,
)


class TestConsultant:
    """Test suite for Consultant class"""

    def test_initialization(self):
        """Test consultant initialization"""
        consultant = Consultant("John Doe", "EMP001", 75.0)
        assert consultant.name == "John Doe"
        assert consultant.employee_id == "EMP001"
        assert consultant.hourly_rate == 75.0

    def test_calculate_earnings(self):
        """Test earnings calculation"""
        consultant = Consultant("John Doe", "EMP001", 75.0)
        assert consultant.calculate_earnings(8.0) == 600.0
        assert consultant.calculate_earnings(10.5) == 787.5

    def test_get_display_name(self):
        """Test display name formatting"""
        consultant = Consultant("John Doe", "EMP001", 75.0)
        assert consultant.get_display_name() == "John Doe (ID: EMP001)"

    def test_str_representation(self):
        """Test string representation"""
        consultant = Consultant("Jane Smith", "EMP002", 80.0)
        result = str(consultant)
        assert "Jane Smith" in result

    def test_repr_representation(self):
        """Test repr representation"""
        consultant = Consultant("Bob", "EMP003", 50.0)
        result = repr(consultant)
        assert "Consultant" in result or "Bob" in result


class TestProject:
    """Test suite for Project class"""

    def test_initialization(self):
        """Test project initialization"""
        project = Project("ACM-101", "Acme Corp", 100.0)
        assert project.code == "ACM-101"
        assert project.client_name == "Acme Corp"
        assert project.budget_hours == 100.0

    def test_is_over_budget_false(self):
        """Test when project is under budget"""
        project = Project("ACM-101", "Acme Corp", 100.0)
        assert project.is_over_budget(80.0) is False
        assert project.is_over_budget(100.0) is False

    def test_is_over_budget_true(self):
        """Test when project is over budget"""
        project = Project("ACM-101", "Acme Corp", 100.0)
        assert project.is_over_budget(101.0) is True
        assert project.is_over_budget(150.0) is True

    def test_remaining_hours_positive(self):
        """Test remaining hours calculation"""
        project = Project("ACM-101", "Acme Corp", 100.0)
        assert project.remaining_hours(60.0) == 40.0
        assert project.remaining_hours(0.0) == 100.0

    def test_remaining_hours_negative(self):
        """Test remaining hours when over budget"""
        project = Project("ACM-101", "Acme Corp", 100.0)
        assert project.remaining_hours(110.0) == -10.0

    def test_str_representation(self):
        """Test string representation"""
        project = Project("BET-5", "Beta Inc", 50.0)
        result = str(project)
        assert "BET-5" in result or "Beta Inc" in result


class TestTimesheetEntry:
    """Test suite for TimesheetEntry class"""

    @pytest.fixture
    def sample_consultant(self):
        return Consultant("John Doe", "EMP001", 75.0)

    @pytest.fixture
    def sample_project(self):
        return Project("ACM-101", "Acme Corp", 100.0)

    def test_initialization(self, sample_consultant, sample_project):
        """Test entry initialization"""
        entry = TimesheetEntry(
            sample_consultant, sample_project, 8.0, "2026-02-10", "Development work"
        )
        assert entry.consultant == sample_consultant
        assert entry.project == sample_project
        assert entry.hours == 8.0
        assert entry.entry_date == "2026-02-10"
        assert entry.description == "Development work"

    def test_calculate_value(self, sample_consultant, sample_project):
        """Test value calculation"""
        entry = TimesheetEntry(sample_consultant, sample_project, 8.0, "2026-02-10")
        assert entry.calculate_value() == 600.0  # 8 * 75

    def test_get_summary(self, sample_consultant, sample_project):
        """Test summary generation"""
        entry = TimesheetEntry(sample_consultant, sample_project, 8.0, "2026-02-10")
        summary = entry.get_summary()
        assert "2026-02-10" in summary
        assert "John Doe" in summary
        assert "ACM-101" in summary
        assert "8" in summary

    def test_is_overtime_false(self, sample_consultant, sample_project):
        """Test overtime detection - false cases"""
        entry = TimesheetEntry(sample_consultant, sample_project, 7.0, "2026-02-10")
        assert entry.is_overtime() is False
        assert entry.is_overtime(8.0) is False

    def test_is_overtime_true(self, sample_consultant, sample_project):
        """Test overtime detection - true cases"""
        entry = TimesheetEntry(sample_consultant, sample_project, 10.0, "2026-02-10")
        assert entry.is_overtime() is True
        assert entry.is_overtime(8.0) is True

    def test_is_overtime_exact_threshold(self, sample_consultant, sample_project):
        """Test overtime at exact threshold"""
        entry = TimesheetEntry(sample_consultant, sample_project, 8.0, "2026-02-10")
        assert entry.is_overtime(8.0) is True

    def test_default_description(self, sample_consultant, sample_project):
        """Test default empty description"""
        entry = TimesheetEntry(sample_consultant, sample_project, 8.0, "2026-02-10")
        assert entry.description == ""


class TestTimesheetManager:
    """Test suite for TimesheetManager class"""

    @pytest.fixture
    def manager(self):
        return TimesheetManager()

    @pytest.fixture
    def sample_entries(self):
        consultant1 = Consultant("John Doe", "EMP001", 75.0)
        consultant2 = Consultant("Jane Smith", "EMP002", 80.0)
        project1 = Project("ACM-101", "Acme Corp", 100.0)
        project2 = Project("BET-5", "Beta Inc", 50.0)

        entries = [
            TimesheetEntry(consultant1, project1, 8.0, "2026-02-10"),
            TimesheetEntry(consultant1, project2, 6.0, "2026-02-11"),
            TimesheetEntry(consultant2, project1, 7.5, "2026-02-12"),
        ]
        return entries

    def test_initialization(self, manager):
        """Test manager initialization"""
        assert manager.get_total_hours() == 0.0

    def test_add_entry(self, manager, sample_entries):
        """Test adding entries"""
        manager.add_entry(sample_entries[0])
        assert manager.get_total_hours() == 8.0

    def test_get_entries_by_consultant(self, manager, sample_entries):
        """Test filtering by consultant"""
        for entry in sample_entries:
            manager.add_entry(entry)

        john_entries = manager.get_entries_by_consultant("John Doe")
        assert len(john_entries) == 2
        assert all(e.consultant.name == "John Doe" for e in john_entries)

    def test_get_entries_by_project(self, manager, sample_entries):
        """Test filtering by project"""
        for entry in sample_entries:
            manager.add_entry(entry)

        acm_entries = manager.get_entries_by_project("ACM-101")
        assert len(acm_entries) == 2
        assert all(e.project.code == "ACM-101" for e in acm_entries)

    def test_get_total_hours(self, manager, sample_entries):
        """Test total hours calculation"""
        for entry in sample_entries:
            manager.add_entry(entry)

        assert manager.get_total_hours() == 21.5  # 8 + 6 + 7.5

    def test_get_total_value(self, manager, sample_entries):
        """Test total value calculation"""
        for entry in sample_entries:
            manager.add_entry(entry)

        # John: 8*75 + 6*75 = 1050, Jane: 7.5*80 = 600
        assert manager.get_total_value() == 1650.0

    def test_get_consultant_summary(self, manager, sample_entries):
        """Test consultant summary"""
        for entry in sample_entries:
            manager.add_entry(entry)

        summary = manager.get_consultant_summary()
        assert summary["John Doe"] == 14.0
        assert summary["Jane Smith"] == 7.5

    def test_empty_manager(self, manager):
        """Test operations on empty manager"""
        assert manager.get_total_hours() == 0.0
        assert manager.get_total_value() == 0.0
        assert manager.get_consultant_summary() == {}


class TestBillableProject:
    """Test suite for BillableProject class"""

    def test_initialization(self):
        """Test billable project initialization"""
        project = BillableProject("ACM-101", "Acme Corp", 100.0, 80.0)
        assert project.code == "ACM-101"
        assert project.client_name == "Acme Corp"
        assert project.budget_hours == 100.0
        assert project.billable_rate == 80.0

    def test_inherits_from_project(self):
        """Test that BillableProject inherits from Project"""
        project = BillableProject("ACM-101", "Acme Corp", 100.0, 80.0)
        assert isinstance(project, Project)

    def test_calculate_billable_hours(self):
        """Test billable hours calculation"""
        project = BillableProject("ACM-101", "Acme Corp", 100.0, 80.0)
        assert project.calculate_billable_hours(40.0) == 32.0  # 40 * 0.8
        assert project.calculate_billable_hours(50.0) == 40.0  # 50 * 0.8

    def test_billable_hours_full_rate(self):
        """Test with 100% billable rate"""
        project = BillableProject("ACM-101", "Acme Corp", 100.0, 100.0)
        assert project.calculate_billable_hours(40.0) == 40.0

    def test_billable_hours_half_rate(self):
        """Test with 50% billable rate"""
        project = BillableProject("ACM-101", "Acme Corp", 100.0, 50.0)
        assert project.calculate_billable_hours(40.0) == 20.0

    def test_calculate_billable_amount(self):
        """Test billable amount calculation"""
        project = BillableProject("ACM-101", "Acme Corp", 100.0, 80.0)
        # 40 hours * 80% = 32 billable hours * 75/hour = 2400
        assert project.calculate_billable_amount(40.0, 75.0) == 2400.0

    def test_project_methods_still_work(self):
        """Test that inherited Project methods still work"""
        project = BillableProject("ACM-101", "Acme Corp", 100.0, 80.0)
        assert project.is_over_budget(50.0) is False
        assert project.remaining_hours(30.0) == 70.0
