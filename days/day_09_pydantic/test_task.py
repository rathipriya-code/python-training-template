"""
Tests for Day 09: Pydantic Models and Validation
"""

import pytest
from datetime import date, timedelta
from pydantic import ValidationError
from .task import (
    ProjectStatus,
    ConsultantCreate,
    Consultant,
    ProjectBase,
    Project,
    TimesheetEntryCreate,
    TimesheetEntry,
    TimesheetSummary,
    BulkTimesheetCreate,
    validate_employee_id,
    validate_project_code,
    create_consultant_from_dict,
    serialize_timesheet_entry,
    validate_timesheet_batch,
)


class TestConsultantModels:
    """Test Consultant Pydantic models"""

    def test_consultant_create_valid(self):
        """Test creating valid consultant"""
        consultant = ConsultantCreate(
            name="John Doe",
            employee_id="EMP001",
            hourly_rate=75.0,
            email="john@example.com",
        )
        assert consultant.name == "John Doe"
        assert consultant.hourly_rate == 75.0

    def test_consultant_with_id(self):
        """Test full consultant model with ID"""
        consultant = Consultant(
            id=1,
            name="Jane Smith",
            employee_id="EMP002",
            hourly_rate=80.0,
            email="jane@example.com",
        )
        assert consultant.id == 1

    def test_consultant_invalid_rate(self):
        """Test that negative rate fails validation"""
        with pytest.raises(ValidationError):
            ConsultantCreate(
                name="John",
                employee_id="EMP001",
                hourly_rate=-50.0,
                email="john@example.com",
            )

    def test_consultant_rate_too_high(self):
        """Test that rate over 1000 fails validation"""
        with pytest.raises(ValidationError):
            ConsultantCreate(
                name="John",
                employee_id="EMP001",
                hourly_rate=1500.0,
                email="john@example.com",
            )

    def test_consultant_name_too_short(self):
        """Test that short name fails validation"""
        with pytest.raises(ValidationError):
            ConsultantCreate(
                name="A", employee_id="EMP001", hourly_rate=75.0, email="a@example.com"
            )


class TestProjectModels:
    """Test Project Pydantic models"""

    def test_project_base_valid(self):
        """Test creating valid project"""
        project = ProjectBase(
            code="ACM-101",
            client_name="Acme Corp",
            budget_hours=100.0,
            status=ProjectStatus.ACTIVE,
        )
        assert project.code == "ACM-101"
        assert project.status == ProjectStatus.ACTIVE

    def test_project_with_hours_used(self):
        """Test full project model"""
        project = Project(
            id=1,
            code="BET-5",
            client_name="Beta Inc",
            budget_hours=50.0,
            status=ProjectStatus.ACTIVE,
            hours_used=25.0,
        )
        assert project.hours_used == 25.0

    def test_project_remaining_hours(self):
        """Test remaining hours calculation"""
        project = Project(
            id=1,
            code="ACM-101",
            client_name="Acme",
            budget_hours=100.0,
            status=ProjectStatus.ACTIVE,
            hours_used=30.0,
        )
        if hasattr(project, "remaining_hours"):
            if callable(project.remaining_hours):
                assert project.remaining_hours() == 70.0
            else:
                assert project.remaining_hours == 70.0

    def test_project_status_enum(self):
        """Test project status enumeration"""
        project = ProjectBase(
            code="TEST-1",
            client_name="Test Client",
            budget_hours=100.0,
            status=ProjectStatus.COMPLETED,
        )
        assert project.status == ProjectStatus.COMPLETED

    def test_project_invalid_budget(self):
        """Test invalid budget hours"""
        with pytest.raises(ValidationError):
            ProjectBase(
                code="TEST-1",
                client_name="Test",
                budget_hours=-10.0,
                status=ProjectStatus.ACTIVE,
            )


class TestTimesheetEntryModels:
    """Test TimesheetEntry Pydantic models"""

    def test_entry_create_valid(self):
        """Test creating valid timesheet entry"""
        entry = TimesheetEntryCreate(
            consultant_id=1,
            project_id=1,
            hours=8.0,
            entry_date=date(2026, 2, 10),
            description="Development work",
        )
        assert entry.hours == 8.0
        assert entry.description == "Development work"

    def test_entry_hours_bounds(self):
        """Test hours validation bounds"""
        # Valid range
        entry = TimesheetEntryCreate(
            consultant_id=1, project_id=1, hours=8.0, entry_date=date(2026, 2, 10)
        )
        assert entry.hours == 8.0

        # Invalid: too low
        with pytest.raises(ValidationError):
            TimesheetEntryCreate(
                consultant_id=1, project_id=1, hours=0.25, entry_date=date(2026, 2, 10)
            )

        # Invalid: too high
        with pytest.raises(ValidationError):
            TimesheetEntryCreate(
                consultant_id=1, project_id=1, hours=30.0, entry_date=date(2026, 2, 10)
            )

    def test_entry_hours_increment(self):
        """Test that hours must be in 0.5 increments"""
        # Valid increments
        valid_hours = [0.5, 1.0, 7.5, 8.0, 8.5]
        for hours in valid_hours:
            entry = TimesheetEntryCreate(
                consultant_id=1, project_id=1, hours=hours, entry_date=date(2026, 2, 10)
            )
            assert entry.hours == hours

        # Invalid increment
        with pytest.raises(ValidationError):
            TimesheetEntryCreate(
                consultant_id=1, project_id=1, hours=7.3, entry_date=date(2026, 2, 10)
            )

    def test_entry_future_date(self):
        """Test that future dates are rejected"""
        future_date = date.today() + timedelta(days=1)
        with pytest.raises(ValidationError):
            TimesheetEntryCreate(
                consultant_id=1, project_id=1, hours=8.0, entry_date=future_date
            )

    def test_entry_optional_description(self):
        """Test that description is optional"""
        entry = TimesheetEntryCreate(
            consultant_id=1, project_id=1, hours=8.0, entry_date=date(2026, 2, 10)
        )
        assert entry.description is None or entry.description == ""


class TestValidationFunctions:
    """Test validation helper functions"""

    def test_validate_employee_id_valid(self):
        """Test valid employee IDs"""
        assert validate_employee_id("EMP001") == "EMP001"
        assert validate_employee_id("EMP12345") == "EMP12345"
        assert validate_employee_id("EMP999") == "EMP999"

    def test_validate_employee_id_invalid(self):
        """Test invalid employee IDs"""
        with pytest.raises(ValueError):
            validate_employee_id("ABC123")

        with pytest.raises(ValueError):
            validate_employee_id("EMP12")  # Too short

        with pytest.raises(ValueError):
            validate_employee_id("EMP1234567")  # Too long

    def test_validate_project_code_valid(self):
        """Test valid project codes"""
        assert validate_project_code("ACM-101") == "ACM-101"
        assert validate_project_code("acm-101") == "ACM-101"  # Converts to uppercase
        assert validate_project_code("BET-5") == "BET-5"

    def test_validate_project_code_normalization(self):
        """Test project code normalization"""
        assert validate_project_code("acm-101") == "ACM-101"
        assert validate_project_code("bet-5") == "BET-5"

    def test_validate_project_code_invalid(self):
        """Test invalid project codes"""
        with pytest.raises(ValueError):
            validate_project_code("AB")  # Too short

        with pytest.raises(ValueError):
            validate_project_code("A" * 25)  # Too long


class TestSerializationFunctions:
    """Test serialization and deserialization"""

    def test_create_consultant_from_dict(self):
        """Test creating consultant from dictionary"""
        data = {
            "id": 1,
            "name": "John Doe",
            "employee_id": "EMP001",
            "hourly_rate": 75.0,
            "email": "john@example.com",
        }
        consultant = create_consultant_from_dict(data)
        assert consultant.id == 1
        assert consultant.name == "John Doe"

    def test_create_consultant_invalid_data(self):
        """Test creating consultant with invalid data raises error"""
        data = {
            "id": 1,
            "name": "X",  # Too short
            "employee_id": "EMP001",
            "hourly_rate": 75.0,
            "email": "john@example.com",
        }
        with pytest.raises(ValidationError):
            create_consultant_from_dict(data)

    def test_serialize_timesheet_entry(self):
        """Test serializing timesheet entry"""
        entry = TimesheetEntry(
            id=1, consultant_id=1, project_id=1, hours=8.0, entry_date=date(2026, 2, 10)
        )
        data = serialize_timesheet_entry(entry)
        assert isinstance(data, dict)
        assert data["id"] == 1
        assert data["hours"] == 8.0


class TestBatchValidation:
    """Test batch validation"""

    def test_validate_all_valid(self):
        """Test validating batch of valid entries"""
        entries = [
            {
                "consultant_id": 1,
                "project_id": 1,
                "hours": 8.0,
                "entry_date": "2026-02-10",
            },
            {
                "consultant_id": 2,
                "project_id": 1,
                "hours": 7.5,
                "entry_date": "2026-02-11",
            },
        ]
        valid, errors = validate_timesheet_batch(entries)
        assert len(valid) == 2
        assert len(errors) == 0

    def test_validate_mixed_batch(self):
        """Test validating batch with some invalid entries"""
        entries = [
            {
                "consultant_id": 1,
                "project_id": 1,
                "hours": 8.0,
                "entry_date": "2026-02-10",
            },
            {
                "consultant_id": 1,
                "project_id": 1,
                "hours": 50.0,  # Invalid: too high
                "entry_date": "2026-02-10",
            },
        ]
        valid, errors = validate_timesheet_batch(entries)
        assert len(valid) == 1
        assert len(errors) == 1

    def test_validate_empty_batch(self):
        """Test validating empty batch"""
        valid, errors = validate_timesheet_batch([])
        assert len(valid) == 0
        assert len(errors) == 0


class TestComplexModels:
    """Test complex nested models"""

    def test_timesheet_summary(self):
        """Test TimesheetSummary model"""
        summary = TimesheetSummary(
            total_entries=10,
            total_hours=80.0,
            consultants=["John", "Jane"],
            projects=["ACM-101", "BET-5"],
            date_range=(date(2026, 2, 1), date(2026, 2, 28)),
        )
        assert summary.total_entries == 10
        assert len(summary.consultants) == 2

    def test_bulk_timesheet_create(self):
        """Test BulkTimesheetCreate model"""
        entries = [
            TimesheetEntryCreate(
                consultant_id=1, project_id=1, hours=8.0, entry_date=date(2026, 2, 10)
            )
        ]
        bulk = BulkTimesheetCreate(
            entries=entries, validate_consultants=True, validate_projects=True
        )
        assert len(bulk.entries) == 1
        assert bulk.validate_consultants is True

    def test_bulk_create_min_entries(self):
        """Test that bulk create requires at least 1 entry"""
        with pytest.raises(ValidationError):
            BulkTimesheetCreate(
                entries=[], validate_consultants=True, validate_projects=True
            )

    def test_bulk_create_max_entries(self):
        """Test that bulk create has max 100 entries"""
        entries = [
            TimesheetEntryCreate(
                consultant_id=1, project_id=1, hours=8.0, entry_date=date(2026, 2, 10)
            )
            for _ in range(101)
        ]
        with pytest.raises(ValidationError):
            BulkTimesheetCreate(
                entries=entries, validate_consultants=True, validate_projects=True
            )
