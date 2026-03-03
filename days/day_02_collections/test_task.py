"""
Tests for Day 02: Lists and Dictionaries
"""

import pytest
from .task import (
    add_timesheet_entry,
    get_total_hours_by_consultant,
    get_projects_for_consultant,
    create_consultant_summary,
    get_entries_by_date_range,
    merge_timesheet_lists,
    update_project_code,
)


class TestAddTimesheetEntry:
    """Test suite for add_timesheet_entry function"""

    def test_add_to_empty_list(self):
        """Test adding entry to empty timesheet list"""
        timesheets = []
        result = add_timesheet_entry(
            timesheets, "John Doe", "ACM-101", 8.0, "2026-02-10"
        )
        assert len(result) == 1
        assert result[0]["consultant"] == "John Doe"
        assert result[0]["project"] == "ACM-101"
        assert result[0]["hours"] == 8.0
        assert result[0]["date"] == "2026-02-10"

    def test_add_multiple_entries(self):
        """Test adding multiple entries"""
        timesheets = []
        result = add_timesheet_entry(
            timesheets, "John Doe", "ACM-101", 8.0, "2026-02-10"
        )
        result = add_timesheet_entry(result, "Jane Smith", "BET-5", 6.5, "2026-02-11")
        assert len(result) == 2
        assert result[1]["consultant"] == "Jane Smith"

    def test_preserves_existing_entries(self):
        """Test that existing entries are preserved"""
        timesheets = [
            {
                "consultant": "Bob",
                "project": "ZET-1",
                "hours": 5.0,
                "date": "2026-02-09",
            }
        ]
        result = add_timesheet_entry(timesheets, "Alice", "XYZ-2", 7.0, "2026-02-10")
        assert len(result) == 2
        assert result[0]["consultant"] == "Bob"


class TestGetTotalHoursByConsultant:
    """Test suite for get_total_hours_by_consultant function"""

    def test_single_consultant_single_entry(self):
        """Test with single entry for one consultant"""
        timesheets = [{"consultant": "John Doe", "hours": 8.0}]
        assert get_total_hours_by_consultant(timesheets, "John Doe") == 8.0

    def test_single_consultant_multiple_entries(self):
        """Test with multiple entries for same consultant"""
        timesheets = [
            {"consultant": "John Doe", "hours": 8.0},
            {"consultant": "John Doe", "hours": 7.5},
            {"consultant": "John Doe", "hours": 6.0},
        ]
        assert get_total_hours_by_consultant(timesheets, "John Doe") == 21.5

    def test_multiple_consultants(self):
        """Test filtering specific consultant from multiple"""
        timesheets = [
            {"consultant": "John Doe", "hours": 8.0},
            {"consultant": "Jane Smith", "hours": 6.0},
            {"consultant": "John Doe", "hours": 7.5},
            {"consultant": "Bob Johnson", "hours": 5.0},
        ]
        assert get_total_hours_by_consultant(timesheets, "John Doe") == 15.5
        assert get_total_hours_by_consultant(timesheets, "Jane Smith") == 6.0

    def test_consultant_not_found(self):
        """Test with consultant that doesn't exist"""
        timesheets = [{"consultant": "John Doe", "hours": 8.0}]
        assert get_total_hours_by_consultant(timesheets, "Jane Smith") == 0.0

    def test_empty_timesheets(self):
        """Test with empty timesheets list"""
        assert get_total_hours_by_consultant([], "John Doe") == 0.0


class TestGetProjectsForConsultant:
    """Test suite for get_projects_for_consultant function"""

    def test_single_project(self):
        """Test consultant working on single project"""
        timesheets = [{"consultant": "John Doe", "project": "ACM-101"}]
        result = get_projects_for_consultant(timesheets, "John Doe")
        assert result == ["ACM-101"]

    def test_multiple_unique_projects(self):
        """Test consultant working on multiple projects"""
        timesheets = [
            {"consultant": "John Doe", "project": "ACM-101"},
            {"consultant": "John Doe", "project": "BET-5"},
            {"consultant": "John Doe", "project": "ZET-99"},
        ]
        result = get_projects_for_consultant(timesheets, "John Doe")
        assert result == ["ACM-101", "BET-5", "ZET-99"]

    def test_duplicate_projects(self):
        """Test that duplicate projects are removed"""
        timesheets = [
            {"consultant": "John Doe", "project": "ACM-101"},
            {"consultant": "John Doe", "project": "BET-5"},
            {"consultant": "John Doe", "project": "ACM-101"},
            {"consultant": "John Doe", "project": "BET-5"},
        ]
        result = get_projects_for_consultant(timesheets, "John Doe")
        assert result == ["ACM-101", "BET-5"]
        assert len(result) == 2

    def test_alphabetical_sorting(self):
        """Test that projects are sorted alphabetically"""
        timesheets = [
            {"consultant": "John Doe", "project": "ZET-99"},
            {"consultant": "John Doe", "project": "ACM-101"},
            {"consultant": "John Doe", "project": "BET-5"},
        ]
        result = get_projects_for_consultant(timesheets, "John Doe")
        assert result == ["ACM-101", "BET-5", "ZET-99"]

    def test_consultant_not_found(self):
        """Test with consultant that doesn't exist"""
        timesheets = [{"consultant": "John Doe", "project": "ACM-101"}]
        result = get_projects_for_consultant(timesheets, "Jane Smith")
        assert result == []


class TestCreateConsultantSummary:
    """Test suite for create_consultant_summary function"""

    def test_single_consultant(self):
        """Test summary for single consultant"""
        timesheets = [
            {"consultant": "John Doe", "hours": 8.0},
            {"consultant": "John Doe", "hours": 7.5},
        ]
        result = create_consultant_summary(timesheets)
        assert result == {"John Doe": 15.5}

    def test_multiple_consultants(self):
        """Test summary for multiple consultants"""
        timesheets = [
            {"consultant": "John Doe", "hours": 8.0},
            {"consultant": "Jane Smith", "hours": 6.0},
            {"consultant": "John Doe", "hours": 7.5},
            {"consultant": "Bob Johnson", "hours": 5.5},
        ]
        result = create_consultant_summary(timesheets)
        assert result == {"John Doe": 15.5, "Jane Smith": 6.0, "Bob Johnson": 5.5}

    def test_empty_timesheets(self):
        """Test with empty timesheets"""
        result = create_consultant_summary([])
        assert result == {}

    def test_decimal_precision(self):
        """Test proper handling of decimal hours"""
        timesheets = [
            {"consultant": "John Doe", "hours": 8.25},
            {"consultant": "John Doe", "hours": 7.75},
        ]
        result = create_consultant_summary(timesheets)
        assert result["John Doe"] == 16.0


class TestGetEntriesByDateRange:
    """Test suite for get_entries_by_date_range function"""

    def test_all_entries_in_range(self):
        """Test when all entries fall within range"""
        timesheets = [
            {"date": "2026-02-10", "hours": 8.0},
            {"date": "2026-02-11", "hours": 7.0},
            {"date": "2026-02-12", "hours": 6.0},
        ]
        result = get_entries_by_date_range(timesheets, "2026-02-10", "2026-02-12")
        assert len(result) == 3

    def test_partial_entries_in_range(self):
        """Test filtering partial entries"""
        timesheets = [
            {"date": "2026-02-01", "hours": 8.0},
            {"date": "2026-02-15", "hours": 7.0},
            {"date": "2026-02-28", "hours": 6.0},
        ]
        result = get_entries_by_date_range(timesheets, "2026-02-10", "2026-02-20")
        assert len(result) == 1
        assert result[0]["date"] == "2026-02-15"

    def test_inclusive_boundaries(self):
        """Test that boundaries are inclusive"""
        timesheets = [
            {"date": "2026-02-10", "hours": 8.0},
            {"date": "2026-02-15", "hours": 7.0},
            {"date": "2026-02-20", "hours": 6.0},
        ]
        result = get_entries_by_date_range(timesheets, "2026-02-10", "2026-02-20")
        assert len(result) == 3

    def test_no_entries_in_range(self):
        """Test when no entries fall in range"""
        timesheets = [
            {"date": "2026-01-15", "hours": 8.0},
            {"date": "2026-03-15", "hours": 7.0},
        ]
        result = get_entries_by_date_range(timesheets, "2026-02-01", "2026-02-28")
        assert len(result) == 0

    def test_single_day_range(self):
        """Test with same start and end date"""
        timesheets = [
            {"date": "2026-02-10", "hours": 8.0},
            {"date": "2026-02-11", "hours": 7.0},
        ]
        result = get_entries_by_date_range(timesheets, "2026-02-10", "2026-02-10")
        assert len(result) == 1
        assert result[0]["date"] == "2026-02-10"


class TestMergeTimesheetLists:
    """Test suite for merge_timesheet_lists function"""

    def test_merge_two_lists(self):
        """Test basic merge of two lists"""
        list1 = [{"id": 1, "hours": 8}]
        list2 = [{"id": 2, "hours": 6}]
        result = merge_timesheet_lists(list1, list2)
        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[1]["id"] == 2

    def test_original_lists_unchanged(self):
        """Test that original lists are not modified"""
        list1 = [{"id": 1, "hours": 8}]
        list2 = [{"id": 2, "hours": 6}]
        result = merge_timesheet_lists(list1, list2)
        assert len(list1) == 1
        assert len(list2) == 1
        assert result is not list1
        assert result is not list2

    def test_merge_with_empty_list(self):
        """Test merging with empty lists"""
        list1 = [{"id": 1, "hours": 8}]
        list2 = []
        result = merge_timesheet_lists(list1, list2)
        assert len(result) == 1

        result2 = merge_timesheet_lists([], list1)
        assert len(result2) == 1

    def test_merge_two_empty_lists(self):
        """Test merging two empty lists"""
        result = merge_timesheet_lists([], [])
        assert result == []

    def test_merge_multiple_entries(self):
        """Test merging lists with multiple entries"""
        list1 = [{"id": 1}, {"id": 2}, {"id": 3}]
        list2 = [{"id": 4}, {"id": 5}]
        result = merge_timesheet_lists(list1, list2)
        assert len(result) == 5


class TestUpdateProjectCode:
    """Test suite for update_project_code function"""

    def test_update_single_entry(self):
        """Test updating a single entry"""
        timesheets = [{"project": "ACM-101", "hours": 8}]
        result = update_project_code(timesheets, "ACM-101", "ACM-102")
        assert timesheets[0]["project"] == "ACM-102"
        assert result is timesheets  # Modified in place

    def test_update_multiple_entries(self):
        """Test updating multiple entries with same project code"""
        timesheets = [
            {"project": "ACM-101", "hours": 8},
            {"project": "BET-5", "hours": 6},
            {"project": "ACM-101", "hours": 7},
        ]
        update_project_code(timesheets, "ACM-101", "ACM-102")
        assert timesheets[0]["project"] == "ACM-102"
        assert timesheets[1]["project"] == "BET-5"  # Unchanged
        assert timesheets[2]["project"] == "ACM-102"

    def test_no_matching_code(self):
        """Test when old code doesn't exist"""
        timesheets = [{"project": "ACM-101", "hours": 8}]
        update_project_code(timesheets, "BET-5", "BET-6")
        assert timesheets[0]["project"] == "ACM-101"  # Unchanged

    def test_empty_timesheets(self):
        """Test with empty timesheets list"""
        timesheets = []
        result = update_project_code(timesheets, "ACM-101", "ACM-102")
        assert result == []
