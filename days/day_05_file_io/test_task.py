"""
Tests for Day 05: File I/O Operations
"""

import pytest
import json
import csv
import tempfile
import shutil
from pathlib import Path
from .task import (
    write_timesheets_to_json,
    read_timesheets_from_json,
    write_timesheets_to_csv,
    read_timesheets_from_csv,
    append_timesheet_to_csv,
    generate_summary_report,
    read_configuration,
    backup_timesheets,
    merge_json_files,
    export_consultant_hours,
)


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files"""
    temp_path = tempfile.mkdtemp()
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.fixture
def sample_timesheets():
    """Sample timesheet data for testing"""
    return [
        {
            "consultant": "John Doe",
            "project": "ACM-101",
            "hours": 8.0,
            "date": "2026-02-10",
        },
        {
            "consultant": "Jane Smith",
            "project": "BET-5",
            "hours": 7.5,
            "date": "2026-02-11",
        },
        {
            "consultant": "John Doe",
            "project": "ACM-101",
            "hours": 6.0,
            "date": "2026-02-12",
        },
    ]


class TestJSONOperations:
    """Test suite for JSON file operations"""

    def test_write_and_read_json(self, temp_dir, sample_timesheets):
        """Test writing and reading JSON files"""
        filepath = Path(temp_dir) / "timesheets.json"
        write_timesheets_to_json(sample_timesheets, str(filepath))

        assert filepath.exists()

        result = read_timesheets_from_json(str(filepath))
        assert len(result) == 3
        assert result[0]["consultant"] == "John Doe"
        assert result[0]["hours"] == 8.0

    def test_write_empty_json(self, temp_dir):
        """Test writing empty list to JSON"""
        filepath = Path(temp_dir) / "empty.json"
        write_timesheets_to_json([], str(filepath))

        result = read_timesheets_from_json(str(filepath))
        assert result == []

    def test_read_nonexistent_json(self):
        """Test reading nonexistent file raises error"""
        with pytest.raises(FileNotFoundError):
            read_timesheets_from_json("nonexistent.json")

    def test_read_invalid_json(self, temp_dir):
        """Test reading invalid JSON raises error"""
        filepath = Path(temp_dir) / "invalid.json"
        filepath.write_text("not valid json{")

        with pytest.raises(json.JSONDecodeError):
            read_timesheets_from_json(str(filepath))

    def test_json_preserves_types(self, temp_dir):
        """Test that JSON preserves data types"""
        filepath = Path(temp_dir) / "types.json"
        data = [{"hours": 8.5, "active": True, "id": 123}]
        write_timesheets_to_json(data, str(filepath))

        result = read_timesheets_from_json(str(filepath))
        assert isinstance(result[0]["hours"], float)
        assert isinstance(result[0]["active"], bool)
        assert isinstance(result[0]["id"], int)


class TestCSVOperations:
    """Test suite for CSV file operations"""

    def test_write_and_read_csv(self, temp_dir, sample_timesheets):
        """Test writing and reading CSV files"""
        filepath = Path(temp_dir) / "timesheets.csv"
        write_timesheets_to_csv(sample_timesheets, str(filepath))

        assert filepath.exists()

        result = read_timesheets_from_csv(str(filepath))
        assert len(result) == 3
        assert result[0]["consultant"] == "John Doe"
        assert isinstance(result[0]["hours"], float)
        assert result[0]["hours"] == 8.0

    def test_csv_headers(self, temp_dir, sample_timesheets):
        """Test that CSV has correct headers"""
        filepath = Path(temp_dir) / "timesheets.csv"
        write_timesheets_to_csv(sample_timesheets, str(filepath))

        with open(filepath, "r") as f:
            reader = csv.DictReader(f)
            assert set(reader.fieldnames) == {"consultant", "project", "hours", "date"}

    def test_write_empty_csv(self, temp_dir):
        """Test writing empty list to CSV"""
        filepath = Path(temp_dir) / "empty.csv"
        write_timesheets_to_csv([], str(filepath))

        result = read_timesheets_from_csv(str(filepath))
        assert result == []

    def test_read_nonexistent_csv(self):
        """Test reading nonexistent CSV raises error"""
        with pytest.raises(FileNotFoundError):
            read_timesheets_from_csv("nonexistent.csv")

    def test_hours_conversion(self, temp_dir):
        """Test that hours are properly converted to float"""
        filepath = Path(temp_dir) / "hours.csv"
        data = [
            {"consultant": "John", "project": "ACM", "hours": 8.5, "date": "2026-02-10"}
        ]
        write_timesheets_to_csv(data, str(filepath))

        result = read_timesheets_from_csv(str(filepath))
        assert isinstance(result[0]["hours"], float)
        assert result[0]["hours"] == 8.5


class TestAppendToCSV:
    """Test suite for append_timesheet_to_csv function"""

    def test_append_to_existing_file(self, temp_dir):
        """Test appending to existing CSV file"""
        filepath = Path(temp_dir) / "append.csv"

        # Create initial file
        initial = [
            {
                "consultant": "John",
                "project": "ACM-101",
                "hours": 8.0,
                "date": "2026-02-10",
            }
        ]
        write_timesheets_to_csv(initial, str(filepath))

        # Append new entry
        new_entry = {
            "consultant": "Jane",
            "project": "BET-5",
            "hours": 7.0,
            "date": "2026-02-11",
        }
        append_timesheet_to_csv(new_entry, str(filepath))

        # Verify
        result = read_timesheets_from_csv(str(filepath))
        assert len(result) == 2
        assert result[1]["consultant"] == "Jane"

    def test_append_creates_new_file(self, temp_dir):
        """Test that append creates file with headers if not exists"""
        filepath = Path(temp_dir) / "new_append.csv"

        entry = {
            "consultant": "John",
            "project": "ACM-101",
            "hours": 8.0,
            "date": "2026-02-10",
        }
        append_timesheet_to_csv(entry, str(filepath))

        assert filepath.exists()
        result = read_timesheets_from_csv(str(filepath))
        assert len(result) == 1
        assert result[0]["consultant"] == "John"

    def test_multiple_appends(self, temp_dir):
        """Test multiple sequential appends"""
        filepath = Path(temp_dir) / "multiple.csv"

        for i in range(3):
            entry = {
                "consultant": f"Person{i}",
                "project": "ACM",
                "hours": 8.0,
                "date": "2026-02-10",
            }
            append_timesheet_to_csv(entry, str(filepath))

        result = read_timesheets_from_csv(str(filepath))
        assert len(result) == 3


class TestGenerateSummaryReport:
    """Test suite for generate_summary_report function"""

    def test_basic_report(self, temp_dir, sample_timesheets):
        """Test generating basic summary report"""
        filepath = Path(temp_dir) / "report.txt"
        generate_summary_report(sample_timesheets, str(filepath))

        assert filepath.exists()
        content = filepath.read_text()

        assert "TIMESHEET SUMMARY REPORT" in content
        assert "Total Entries: 3" in content
        assert "Total Hours: 21.5" in content
        assert "John Doe" in content
        assert "Jane Smith" in content

    def test_report_format(self, temp_dir, sample_timesheets):
        """Test report formatting"""
        filepath = Path(temp_dir) / "report.txt"
        generate_summary_report(sample_timesheets, str(filepath))

        content = filepath.read_text()
        assert "By Consultant:" in content
        assert "John Doe: 14.0 hours" in content
        assert "Jane Smith: 7.5 hours" in content

    def test_empty_report(self, temp_dir):
        """Test report with empty timesheets"""
        filepath = Path(temp_dir) / "empty_report.txt"
        generate_summary_report([], str(filepath))

        content = filepath.read_text()
        assert "Total Entries: 0" in content
        assert "Total Hours: 0.0" in content


class TestReadConfiguration:
    """Test suite for read_configuration function"""

    def test_read_existing_config(self, temp_dir):
        """Test reading existing configuration"""
        filepath = Path(temp_dir) / "config.json"
        config_data = {"standard_hours": 35.0, "overtime_multiplier": 2.0}
        filepath.write_text(json.dumps(config_data))

        config = read_configuration(str(filepath))
        assert config["standard_hours"] == 35.0
        assert config["overtime_multiplier"] == 2.0

    def test_missing_config_returns_defaults(self, temp_dir):
        """Test that missing config file returns defaults"""
        filepath = Path(temp_dir) / "nonexistent.json"

        config = read_configuration(str(filepath))
        assert config["standard_hours"] == 40.0
        assert config["overtime_multiplier"] == 1.5
        assert config["billable_rate"] == 75.0

    def test_default_config_structure(self, temp_dir):
        """Test default configuration has all required keys"""
        config = read_configuration("nonexistent_file.json")
        assert "standard_hours" in config
        assert "overtime_multiplier" in config
        assert "billable_rate" in config


class TestBackupTimesheets:
    """Test suite for backup_timesheets function"""

    def test_basic_backup(self, temp_dir, sample_timesheets):
        """Test creating a backup"""
        source_file = Path(temp_dir) / "source.json"
        backup_dir = Path(temp_dir) / "backups"
        backup_dir.mkdir()

        write_timesheets_to_json(sample_timesheets, str(source_file))

        backup_path = backup_timesheets(
            str(source_file), str(backup_dir), "backup.json"
        )

        assert Path(backup_path).exists()
        backup_data = read_timesheets_from_json(backup_path)
        assert len(backup_data) == 3

    def test_backup_nonexistent_source(self, temp_dir):
        """Test backing up nonexistent file raises error"""
        backup_dir = Path(temp_dir) / "backups"
        backup_dir.mkdir()

        with pytest.raises(FileNotFoundError):
            backup_timesheets("nonexistent.json", str(backup_dir), "backup.json")

    def test_backup_creates_directory(self, temp_dir, sample_timesheets):
        """Test that backup creates directory if needed"""
        source_file = Path(temp_dir) / "source.json"
        backup_dir = Path(temp_dir) / "new_backups"

        write_timesheets_to_json(sample_timesheets, str(source_file))

        backup_path = backup_timesheets(
            str(source_file), str(backup_dir), "backup.json"
        )

        assert Path(backup_dir).exists()
        assert Path(backup_path).exists()


class TestMergeJSONFiles:
    """Test suite for merge_json_files function"""

    def test_merge_two_files(self, temp_dir):
        """Test merging two JSON files"""
        file1 = Path(temp_dir) / "file1.json"
        file2 = Path(temp_dir) / "file2.json"
        output = Path(temp_dir) / "merged.json"

        data1 = [{"consultant": "John", "hours": 8}]
        data2 = [{"consultant": "Jane", "hours": 7}]

        write_timesheets_to_json(data1, str(file1))
        write_timesheets_to_json(data2, str(file2))

        count = merge_json_files([str(file1), str(file2)], str(output))

        assert count == 2
        merged = read_timesheets_from_json(str(output))
        assert len(merged) == 2

    def test_merge_skips_nonexistent(self, temp_dir):
        """Test that merge skips nonexistent files"""
        file1 = Path(temp_dir) / "file1.json"
        output = Path(temp_dir) / "merged.json"

        data1 = [{"consultant": "John", "hours": 8}]
        write_timesheets_to_json(data1, str(file1))

        count = merge_json_files([str(file1), "nonexistent.json"], str(output))

        assert count == 1

    def test_merge_empty_list(self, temp_dir):
        """Test merging empty list of files"""
        output = Path(temp_dir) / "merged.json"

        count = merge_json_files([], str(output))

        assert count == 0
        merged = read_timesheets_from_json(str(output))
        assert merged == []


class TestExportConsultantHours:
    """Test suite for export_consultant_hours function"""

    def test_export_single_consultant(self, temp_dir, sample_timesheets):
        """Test exporting hours for specific consultant"""
        output = Path(temp_dir) / "john_hours.txt"

        export_consultant_hours(sample_timesheets, "John Doe", str(output))

        assert output.exists()
        content = output.read_text()
        lines = content.strip().split("\n")

        assert len(lines) == 2  # John has 2 entries
        assert "2026-02-10" in lines[0]
        assert "ACM-101" in lines[0]
        assert "8.0 hours" in lines[0]

    def test_export_format(self, temp_dir, sample_timesheets):
        """Test export format is correct"""
        output = Path(temp_dir) / "export.txt"

        export_consultant_hours(sample_timesheets, "Jane Smith", str(output))

        content = output.read_text().strip()
        assert "2026-02-11 | BET-5 | 7.5 hours" in content

    def test_export_nonexistent_consultant(self, temp_dir, sample_timesheets):
        """Test exporting for consultant not in data"""
        output = Path(temp_dir) / "export.txt"

        export_consultant_hours(sample_timesheets, "Bob Johnson", str(output))

        content = output.read_text().strip()
        assert content == "" or not output.exists() or output.stat().st_size == 0
