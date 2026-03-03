"""
Tests for Day 07: Week 1 Integration Project
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from .task import (
    TimesheetApp,
    create_sample_data,
)


@pytest.fixture
def temp_dir():
    """Create temporary directory for test files"""
    temp_path = tempfile.mkdtemp()
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.fixture
def app(temp_dir):
    """Create app instance with temporary data file"""
    data_file = Path(temp_dir) / "test_timesheets.json"
    return TimesheetApp(str(data_file))


@pytest.fixture
def populated_app(app):
    """App with sample data"""
    app.add_entry("John Doe", "ACM-101", 8.0, "2026-02-10", "Backend development")
    app.add_entry("John Doe", "ACM-101", 7.5, "2026-02-11", "API implementation")
    app.add_entry("Jane Smith", "BET-5", 6.0, "2026-02-10", "Frontend work")
    app.add_entry("Bob Johnson", "ACM-101", 9.0, "2026-02-12", "Database optimization")
    app.add_entry("Jane Smith", "ZET-99", 8.5, "2026-02-13", "Testing")
    return app


class TestTimesheetAppBasics:
    """Test basic app functionality"""

    def test_initialization(self, app):
        """Test app initializes correctly"""
        assert app is not None
        assert hasattr(app, "timesheets")

    def test_add_valid_entry(self, app):
        """Test adding valid entry"""
        result = app.add_entry("John Doe", "ACM-101", 8.0, "2026-02-10")
        assert result is True
        assert len(app.timesheets) == 1

    def test_add_invalid_hours(self, app):
        """Test adding entry with invalid hours"""
        result = app.add_entry("John Doe", "ACM-101", -5.0, "2026-02-10")
        assert result is False
        assert len(app.timesheets) == 0

    def test_add_empty_consultant(self, app):
        """Test adding entry with empty consultant"""
        result = app.add_entry("", "ACM-101", 8.0, "2026-02-10")
        assert result is False

    def test_add_empty_project(self, app):
        """Test adding entry with empty project"""
        result = app.add_entry("John Doe", "", 8.0, "2026-02-10")
        assert result is False

    def test_add_invalid_date(self, app):
        """Test adding entry with invalid date"""
        result = app.add_entry("John Doe", "ACM-101", 8.0, "invalid-date")
        assert result is False


class TestDataPersistence:
    """Test data loading and saving"""

    def test_save_and_load(self, app):
        """Test saving and loading data"""
        app.add_entry("John Doe", "ACM-101", 8.0, "2026-02-10")
        app.add_entry("Jane Smith", "BET-5", 7.0, "2026-02-11")

        # Save data
        result = app.save_data()
        assert result is True

        # Create new app instance and load
        new_app = TimesheetApp(app.data_file)
        loaded = new_app.load_data()

        assert len(loaded) == 2
        assert loaded[0]["consultant"] == "John Doe"

    def test_load_nonexistent_file(self, app):
        """Test loading from nonexistent file returns empty list"""
        data = app.load_data()
        assert data == []

    def test_save_creates_file(self, app, temp_dir):
        """Test that save creates file"""
        app.add_entry("John Doe", "ACM-101", 8.0, "2026-02-10")
        app.save_data()

        assert Path(app.data_file).exists()


class TestQueryFunctions:
    """Test query and filter functions"""

    def test_get_entries_by_consultant(self, populated_app):
        """Test filtering by consultant"""
        entries = populated_app.get_entries_by_consultant("John Doe")
        assert len(entries) == 2
        assert all(e["consultant"] == "John Doe" for e in entries)

    def test_get_entries_nonexistent_consultant(self, populated_app):
        """Test filtering by nonexistent consultant"""
        entries = populated_app.get_entries_by_consultant("Nobody")
        assert entries == []

    def test_get_entries_by_date_range(self, populated_app):
        """Test filtering by date range"""
        entries = populated_app.get_entries_by_date_range("2026-02-10", "2026-02-11")
        assert len(entries) == 3

    def test_get_entries_date_range_exclusive(self, populated_app):
        """Test date range boundaries"""
        entries = populated_app.get_entries_by_date_range("2026-02-11", "2026-02-12")
        assert len(entries) == 2

    def test_calculate_total_hours_all(self, populated_app):
        """Test calculating total hours for all"""
        total = populated_app.calculate_total_hours()
        assert total == 39.0  # 8 + 7.5 + 6 + 9 + 8.5

    def test_calculate_total_hours_by_consultant(self, populated_app):
        """Test calculating hours for specific consultant"""
        total = populated_app.calculate_total_hours("John Doe")
        assert total == 15.5  # 8 + 7.5

    def test_calculate_hours_nonexistent_consultant(self, populated_app):
        """Test calculating hours for nonexistent consultant"""
        total = populated_app.calculate_total_hours("Nobody")
        assert total == 0.0


class TestSummaryFunctions:
    """Test summary generation functions"""

    def test_get_consultant_summary(self, populated_app):
        """Test consultant summary generation"""
        summary = populated_app.get_consultant_summary()

        assert "John Doe" in summary
        assert summary["John Doe"]["total_hours"] == 15.5
        assert summary["John Doe"]["entry_count"] == 2
        assert "ACM-101" in summary["John Doe"]["projects"]

    def test_consultant_summary_projects_sorted(self, populated_app):
        """Test that projects in summary are sorted"""
        summary = populated_app.get_consultant_summary()
        jane_projects = summary["Jane Smith"]["projects"]
        assert jane_projects == sorted(jane_projects)

    def test_get_project_summary(self, populated_app):
        """Test project summary generation"""
        summary = populated_app.get_project_summary()

        assert "ACM-101" in summary
        assert summary["ACM-101"]["total_hours"] == 24.5  # 8 + 7.5 + 9
        assert summary["ACM-101"]["entry_count"] == 3
        assert len(summary["ACM-101"]["consultants"]) == 2

    def test_project_summary_consultants_sorted(self, populated_app):
        """Test that consultants in summary are sorted"""
        summary = populated_app.get_project_summary()
        consultants = summary["ACM-101"]["consultants"]
        assert consultants == sorted(consultants)


class TestExportFunctions:
    """Test export functionality"""

    def test_export_to_csv_all(self, populated_app, temp_dir):
        """Test exporting all entries to CSV"""
        output_file = Path(temp_dir) / "export.csv"
        count = populated_app.export_to_csv(str(output_file))

        assert count == 5
        assert output_file.exists()

    def test_export_to_csv_filtered(self, populated_app, temp_dir):
        """Test exporting filtered entries to CSV"""
        output_file = Path(temp_dir) / "export_john.csv"
        count = populated_app.export_to_csv(str(output_file), consultant="John Doe")

        assert count == 2
        assert output_file.exists()

    def test_generate_report(self, populated_app, temp_dir):
        """Test report generation"""
        output_file = Path(temp_dir) / "report.txt"
        populated_app.generate_report(str(output_file))

        assert output_file.exists()
        content = output_file.read_text()

        assert "TIMESHEET REPORT" in content
        assert "Total Entries: 5" in content
        assert "Total Hours: 39.0" in content
        assert "CONSULTANT SUMMARY" in content
        assert "PROJECT SUMMARY" in content


class TestAdvancedFeatures:
    """Test advanced features"""

    def test_find_overtime_entries(self, populated_app):
        """Test finding overtime entries"""
        overtime = populated_app.find_overtime_entries(8.0)

        # Should find entries with hours >= 8.0
        assert len(overtime) >= 3
        assert all(e["hours"] >= 8.0 for e in overtime)

    def test_find_overtime_custom_threshold(self, populated_app):
        """Test overtime with custom threshold"""
        overtime = populated_app.find_overtime_entries(9.0)

        # Should find entries with hours >= 9.0
        assert all(e["hours"] >= 9.0 for e in overtime)

    def test_get_top_consultants(self, populated_app):
        """Test getting top consultants"""
        top = populated_app.get_top_consultants(limit=2)

        assert len(top) == 2
        # Should be sorted by hours descending
        assert top[0][1] >= top[1][1]

    def test_top_consultants_data(self, populated_app):
        """Test top consultants returns correct data"""
        top = populated_app.get_top_consultants(limit=5)

        # John: 15.5, Jane: 14.5, Bob: 9.0
        assert len(top) == 3
        names = [name for name, hours in top]
        assert "John Doe" in names
        assert "Jane Smith" in names


class TestValidation:
    """Test validation functions"""

    def test_validate_valid_entry(self, app):
        """Test validation of valid entry"""
        is_valid, error = app.validate_entry_data(
            "John Doe", "ACM-101", 8.0, "2026-02-10"
        )
        assert is_valid is True
        assert error == ""

    def test_validate_invalid_hours(self, app):
        """Test validation catches invalid hours"""
        is_valid, error = app.validate_entry_data(
            "John Doe", "ACM-101", -5.0, "2026-02-10"
        )
        assert is_valid is False
        assert error != ""

    def test_validate_empty_consultant(self, app):
        """Test validation catches empty consultant"""
        is_valid, error = app.validate_entry_data("", "ACM-101", 8.0, "2026-02-10")
        assert is_valid is False
        assert "consultant" in error.lower() or "empty" in error.lower()

    def test_validate_invalid_date(self, app):
        """Test validation catches invalid date"""
        is_valid, error = app.validate_entry_data(
            "John Doe", "ACM-101", 8.0, "bad-date"
        )
        assert is_valid is False
        assert "date" in error.lower()


class TestBulkOperations:
    """Test bulk operations"""

    def test_bulk_import_valid(self, app, temp_dir):
        """Test bulk import with valid data"""
        import_file = Path(temp_dir) / "import.json"
        data = [
            {
                "consultant": "John",
                "project": "ACM-101",
                "hours": 8.0,
                "date": "2026-02-10",
            },
            {
                "consultant": "Jane",
                "project": "BET-5",
                "hours": 7.0,
                "date": "2026-02-11",
            },
        ]
        import_file.write_text(json.dumps(data))

        success, failed, errors = app.bulk_import_from_json(str(import_file))

        assert success == 2
        assert failed == 0
        assert len(errors) == 0

    def test_bulk_import_mixed(self, app, temp_dir):
        """Test bulk import with mixed valid/invalid data"""
        import_file = Path(temp_dir) / "import.json"
        data = [
            {
                "consultant": "John",
                "project": "ACM-101",
                "hours": 8.0,
                "date": "2026-02-10",
            },
            {"consultant": "", "project": "BET-5", "hours": 7.0, "date": "2026-02-11"},
            {
                "consultant": "Jane",
                "project": "ZET-99",
                "hours": 6.0,
                "date": "2026-02-12",
            },
        ]
        import_file.write_text(json.dumps(data))

        success, failed, errors = app.bulk_import_from_json(str(import_file))

        assert success == 2
        assert failed == 1
        assert len(errors) == 1

    def test_delete_entries_by_consultant(self, populated_app):
        """Test deleting entries by consultant"""
        initial_count = len(populated_app.timesheets)
        deleted = populated_app.delete_entries_by_consultant("John Doe")

        assert deleted == 2
        assert len(populated_app.timesheets) == initial_count - 2

        # Verify John's entries are gone
        remaining = populated_app.get_entries_by_consultant("John Doe")
        assert len(remaining) == 0

    def test_update_project_code(self, populated_app):
        """Test updating project code"""
        updated = populated_app.update_project_code("ACM-101", "ACM-102")

        assert updated == 3  # Three entries had ACM-101

        # Verify old code is gone
        old_entries = [e for e in populated_app.timesheets if e["project"] == "ACM-101"]
        assert len(old_entries) == 0

        # Verify new code exists
        new_entries = [e for e in populated_app.timesheets if e["project"] == "ACM-102"]
        assert len(new_entries) == 3


class TestHelperFunctions:
    """Test helper functions"""

    def test_create_sample_data(self):
        """Test sample data creation"""
        data = create_sample_data()

        assert isinstance(data, list)
        assert len(data) > 0
        assert all("consultant" in entry for entry in data)
        assert all("project" in entry for entry in data)
        assert all("hours" in entry for entry in data)
        assert all("date" in entry for entry in data)
