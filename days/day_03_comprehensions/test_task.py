"""
Tests for Day 03: Comprehensions
"""

import pytest
from .task import (
    extract_consultant_names,
    get_high_hour_entries,
    calculate_daily_totals,
    get_billable_hours_map,
    extract_unique_projects,
    create_consultant_project_matrix,
    transform_to_uppercase_projects,
    filter_and_transform,
    nested_hours_by_consultant_and_project,
)


class TestExtractConsultantNames:
    """Test suite for extract_consultant_names function"""

    def test_basic_extraction(self):
        """Test basic name extraction"""
        timesheets = [
            {"consultant": "John Doe", "hours": 8},
            {"consultant": "Jane Smith", "hours": 6},
        ]
        result = extract_consultant_names(timesheets)
        assert result == ["John Doe", "Jane Smith"]

    def test_with_duplicates(self):
        """Test that duplicates are preserved"""
        timesheets = [
            {"consultant": "John Doe", "hours": 8},
            {"consultant": "Jane Smith", "hours": 6},
            {"consultant": "John Doe", "hours": 7},
        ]
        result = extract_consultant_names(timesheets)
        assert len(result) == 3
        assert result.count("John Doe") == 2

    def test_empty_list(self):
        """Test with empty timesheets"""
        assert extract_consultant_names([]) == []


class TestGetHighHourEntries:
    """Test suite for get_high_hour_entries function"""

    def test_basic_filtering(self):
        """Test basic hour filtering"""
        timesheets = [
            {"consultant": "John", "hours": 8.0},
            {"consultant": "Jane", "hours": 4.0},
            {"consultant": "Bob", "hours": 10.0},
        ]
        result = get_high_hour_entries(timesheets, 7.0)
        assert len(result) == 2
        assert result[0]["consultant"] == "John"
        assert result[1]["consultant"] == "Bob"

    def test_exact_threshold(self):
        """Test entries at exact threshold"""
        timesheets = [
            {"consultant": "John", "hours": 8.0},
            {"consultant": "Jane", "hours": 8.0},
        ]
        result = get_high_hour_entries(timesheets, 8.0)
        assert len(result) == 2

    def test_no_matches(self):
        """Test when no entries meet threshold"""
        timesheets = [{"consultant": "John", "hours": 5.0}]
        result = get_high_hour_entries(timesheets, 10.0)
        assert result == []

    def test_all_match(self):
        """Test when all entries meet threshold"""
        timesheets = [
            {"consultant": "John", "hours": 8.0},
            {"consultant": "Jane", "hours": 9.0},
        ]
        result = get_high_hour_entries(timesheets, 5.0)
        assert len(result) == 2


class TestCalculateDailyTotals:
    """Test suite for calculate_daily_totals function"""

    def test_single_date(self):
        """Test with entries on single date"""
        timesheets = [
            {"date": "2026-02-10", "hours": 8.0},
            {"date": "2026-02-10", "hours": 6.0},
        ]
        result = calculate_daily_totals(timesheets)
        assert result == {"2026-02-10": 14.0}

    def test_multiple_dates(self):
        """Test with multiple dates"""
        timesheets = [
            {"date": "2026-02-10", "hours": 8.0},
            {"date": "2026-02-10", "hours": 6.0},
            {"date": "2026-02-11", "hours": 7.0},
            {"date": "2026-02-11", "hours": 5.0},
        ]
        result = calculate_daily_totals(timesheets)
        assert result == {"2026-02-10": 14.0, "2026-02-11": 12.0}

    def test_single_entry_per_date(self):
        """Test with one entry per date"""
        timesheets = [
            {"date": "2026-02-10", "hours": 8.0},
            {"date": "2026-02-11", "hours": 7.0},
        ]
        result = calculate_daily_totals(timesheets)
        assert result == {"2026-02-10": 8.0, "2026-02-11": 7.0}

    def test_empty_timesheets(self):
        """Test with empty timesheets"""
        result = calculate_daily_totals([])
        assert result == {}


class TestGetBillableHoursMap:
    """Test suite for get_billable_hours_map function"""

    def test_basic_calculation(self):
        """Test basic billable hours calculation"""
        timesheets = [
            {"consultant": "John", "hours": 40.0},
            {"consultant": "Jane", "hours": 30.0},
        ]
        result = get_billable_hours_map(timesheets, 80.0)
        assert result == {"John": 32.0, "Jane": 24.0}

    def test_aggregation(self):
        """Test aggregation of multiple entries"""
        timesheets = [
            {"consultant": "John", "hours": 40.0},
            {"consultant": "Jane", "hours": 30.0},
            {"consultant": "John", "hours": 10.0},
        ]
        result = get_billable_hours_map(timesheets, 80.0)
        assert result == {"John": 40.0, "Jane": 24.0}

    def test_full_billable(self):
        """Test with 100% billable rate"""
        timesheets = [{"consultant": "John", "hours": 40.0}]
        result = get_billable_hours_map(timesheets, 100.0)
        assert result == {"John": 40.0}

    def test_fifty_percent(self):
        """Test with 50% billable rate"""
        timesheets = [{"consultant": "John", "hours": 40.0}]
        result = get_billable_hours_map(timesheets, 50.0)
        assert result == {"John": 20.0}


class TestExtractUniqueProjects:
    """Test suite for extract_unique_projects function"""

    def test_unique_projects(self):
        """Test extraction of unique projects"""
        timesheets = [
            {"project": "ACM-101"},
            {"project": "BET-5"},
            {"project": "ACM-101"},
        ]
        result = extract_unique_projects(timesheets)
        assert result == {"ACM-101", "BET-5"}

    def test_all_unique(self):
        """Test when all projects are unique"""
        timesheets = [
            {"project": "ACM-101"},
            {"project": "BET-5"},
            {"project": "ZET-99"},
        ]
        result = extract_unique_projects(timesheets)
        assert len(result) == 3

    def test_single_project(self):
        """Test with single project"""
        timesheets = [{"project": "ACM-101"}]
        result = extract_unique_projects(timesheets)
        assert result == {"ACM-101"}

    def test_empty_timesheets(self):
        """Test with empty timesheets"""
        result = extract_unique_projects([])
        assert result == set()


class TestCreateConsultantProjectMatrix:
    """Test suite for create_consultant_project_matrix function"""

    def test_basic_matrix(self):
        """Test basic consultant-project matrix"""
        timesheets = [
            {"consultant": "John", "project": "ACM-101"},
            {"consultant": "John", "project": "BET-5"},
            {"consultant": "Jane", "project": "ACM-101"},
        ]
        result = create_consultant_project_matrix(timesheets)
        assert result["John"] == ["ACM-101", "BET-5"]
        assert result["Jane"] == ["ACM-101"]

    def test_duplicate_removal(self):
        """Test that duplicate projects are removed"""
        timesheets = [
            {"consultant": "John", "project": "ACM-101"},
            {"consultant": "John", "project": "ACM-101"},
        ]
        result = create_consultant_project_matrix(timesheets)
        assert result["John"] == ["ACM-101"]

    def test_alphabetical_sorting(self):
        """Test that projects are sorted alphabetically"""
        timesheets = [
            {"consultant": "John", "project": "ZET-99"},
            {"consultant": "John", "project": "ACM-101"},
            {"consultant": "John", "project": "BET-5"},
        ]
        result = create_consultant_project_matrix(timesheets)
        assert result["John"] == ["ACM-101", "BET-5", "ZET-99"]

    def test_multiple_consultants(self):
        """Test with multiple consultants"""
        timesheets = [
            {"consultant": "John", "project": "ACM-101"},
            {"consultant": "Jane", "project": "BET-5"},
            {"consultant": "Bob", "project": "ZET-99"},
        ]
        result = create_consultant_project_matrix(timesheets)
        assert len(result) == 3


class TestTransformToUppercaseProjects:
    """Test suite for transform_to_uppercase_projects function"""

    def test_basic_transformation(self):
        """Test basic uppercase transformation"""
        timesheets = [
            {"consultant": "John", "project": "acm-101", "hours": 8},
            {"consultant": "Jane", "project": "bet-5", "hours": 6},
        ]
        result = transform_to_uppercase_projects(timesheets)
        assert result[0]["project"] == "ACM-101"
        assert result[1]["project"] == "BET-5"

    def test_preserves_other_fields(self):
        """Test that other fields are preserved"""
        timesheets = [{"consultant": "John", "project": "acm-101", "hours": 8}]
        result = transform_to_uppercase_projects(timesheets)
        assert result[0]["consultant"] == "John"
        assert result[0]["hours"] == 8

    def test_already_uppercase(self):
        """Test with already uppercase projects"""
        timesheets = [{"consultant": "John", "project": "ACM-101", "hours": 8}]
        result = transform_to_uppercase_projects(timesheets)
        assert result[0]["project"] == "ACM-101"

    def test_mixed_case(self):
        """Test with mixed case"""
        timesheets = [{"consultant": "John", "project": "AcM-101", "hours": 8}]
        result = transform_to_uppercase_projects(timesheets)
        assert result[0]["project"] == "ACM-101"


class TestFilterAndTransform:
    """Test suite for filter_and_transform function"""

    def test_both_conditions(self):
        """Test filtering with both conditions"""
        timesheets = [
            {"consultant": "John", "project": "ACM-101", "hours": 8},
            {"consultant": "Jane", "project": "BET-5", "hours": 9},
            {"consultant": "Bob", "project": "ACM-102", "hours": 6},
        ]
        result = filter_and_transform(timesheets, 7.0, "ACM")
        assert result == ["John"]

    def test_multiple_matches(self):
        """Test with multiple matching entries"""
        timesheets = [
            {"consultant": "John", "project": "ACM-101", "hours": 8},
            {"consultant": "Jane", "project": "ACM-102", "hours": 9},
            {"consultant": "Bob", "project": "BET-5", "hours": 10},
        ]
        result = filter_and_transform(timesheets, 7.0, "ACM")
        assert len(result) == 2
        assert "John" in result
        assert "Jane" in result

    def test_no_matches(self):
        """Test when no entries match both conditions"""
        timesheets = [
            {"consultant": "John", "project": "BET-5", "hours": 8},
            {"consultant": "Jane", "project": "ACM-101", "hours": 5},
        ]
        result = filter_and_transform(timesheets, 7.0, "ACM")
        assert result == []

    def test_prefix_matching(self):
        """Test prefix matching works correctly"""
        timesheets = [
            {"consultant": "John", "project": "ACM-101", "hours": 8},
            {"consultant": "Jane", "project": "ACME-5", "hours": 8},
        ]
        result = filter_and_transform(timesheets, 7.0, "ACM")
        assert len(result) == 2  # Both start with ACM


class TestNestedHoursByConsultantAndProject:
    """Test suite for nested_hours_by_consultant_and_project function"""

    def test_basic_nesting(self):
        """Test basic nested dictionary creation"""
        timesheets = [
            {"consultant": "John", "project": "ACM-101", "hours": 8},
            {"consultant": "John", "project": "BET-5", "hours": 6},
        ]
        result = nested_hours_by_consultant_and_project(timesheets)
        assert result["John"]["ACM-101"] == 8.0
        assert result["John"]["BET-5"] == 6.0

    def test_aggregation(self):
        """Test aggregation of hours for same consultant and project"""
        timesheets = [
            {"consultant": "John", "project": "ACM-101", "hours": 8},
            {"consultant": "John", "project": "ACM-101", "hours": 7},
            {"consultant": "John", "project": "BET-5", "hours": 6},
        ]
        result = nested_hours_by_consultant_and_project(timesheets)
        assert result["John"]["ACM-101"] == 15.0
        assert result["John"]["BET-5"] == 6.0

    def test_multiple_consultants(self):
        """Test with multiple consultants"""
        timesheets = [
            {"consultant": "John", "project": "ACM-101", "hours": 8},
            {"consultant": "Jane", "project": "ACM-101", "hours": 6},
        ]
        result = nested_hours_by_consultant_and_project(timesheets)
        assert result["John"]["ACM-101"] == 8.0
        assert result["Jane"]["ACM-101"] == 6.0

    def test_complex_scenario(self):
        """Test complex scenario with multiple consultants and projects"""
        timesheets = [
            {"consultant": "John", "project": "ACM-101", "hours": 8},
            {"consultant": "John", "project": "BET-5", "hours": 6},
            {"consultant": "Jane", "project": "ACM-101", "hours": 7},
            {"consultant": "Jane", "project": "ACM-101", "hours": 5},
        ]
        result = nested_hours_by_consultant_and_project(timesheets)
        assert result["John"]["ACM-101"] == 8.0
        assert result["John"]["BET-5"] == 6.0
        assert result["Jane"]["ACM-101"] == 12.0
