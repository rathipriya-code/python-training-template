"""
Tests for Day 04: Error Handling and Exceptions
"""

import pytest
from .task import (
    TimesheetValidationError,
    InvalidHoursError,
    InvalidDateError,
    validate_hours,
    safe_divide_hours,
    parse_date,
    validate_and_create_entry,
    safe_get_nested_value,
    process_timesheet_batch,
    calculate_with_fallback,
    guaranteed_cleanup_operation,
)


class TestValidateHours:
    """Test suite for validate_hours function"""
    
    def test_valid_hours(self):
        """Test validation with valid hours"""
        assert validate_hours(8.0) == 8.0
        assert validate_hours(0.5) == 0.5
        assert validate_hours(24.0) == 24.0
    
    def test_negative_hours(self):
        """Test that negative hours raise error"""
        with pytest.raises(InvalidHoursError, match="Hours must be between 0.5 and 24.0"):
            validate_hours(-5.0)
    
    def test_zero_hours(self):
        """Test that zero hours raise error"""
        with pytest.raises(InvalidHoursError, match="Hours must be between 0.5 and 24.0"):
            validate_hours(0.0)
    
    def test_below_minimum(self):
        """Test hours below minimum threshold"""
        with pytest.raises(InvalidHoursError):
            validate_hours(0.25)
    
    def test_above_maximum(self):
        """Test hours above 24"""
        with pytest.raises(InvalidHoursError, match="Hours must be between 0.5 and 24.0"):
            validate_hours(25.0)
    
    def test_non_numeric_type(self):
        """Test with non-numeric input"""
        with pytest.raises(TypeError):
            validate_hours("8")  # type: ignore


class TestSafeDivideHours:
    """Test suite for safe_divide_hours function"""
    
    def test_valid_division(self):
        """Test normal division"""
        assert safe_divide_hours(40.0, 5) == 8.0
        assert safe_divide_hours(35.5, 5) == 7.1
    
    def test_division_by_zero(self):
        """Test that division by zero returns None"""
        result = safe_divide_hours(40.0, 0)
        assert result is None
    
    def test_zero_hours(self):
        """Test with zero hours"""
        assert safe_divide_hours(0.0, 5) == 0.0
    
    def test_decimal_result(self):
        """Test that decimal results are preserved"""
        result = safe_divide_hours(25.0, 3)
        assert abs(result - 8.333333) < 0.001


class TestParseDate:
    """Test suite for parse_date function"""
    
    def test_valid_date(self):
        """Test parsing valid dates"""
        assert parse_date("2026-02-10") == (2026, 2, 10)
        assert parse_date("2025-12-31") == (2025, 12, 31)
        assert parse_date("2026-01-01") == (2026, 1, 1)
    
    def test_invalid_month(self):
        """Test invalid month values"""
        with pytest.raises(InvalidDateError, match="Month must be between 1 and 12"):
            parse_date("2026-13-01")
        with pytest.raises(InvalidDateError, match="Month must be between 1 and 12"):
            parse_date("2026-00-01")
    
    def test_invalid_day(self):
        """Test invalid day values"""
        with pytest.raises(InvalidDateError, match="Day must be between 1 and 31"):
            parse_date("2026-02-32")
        with pytest.raises(InvalidDateError, match="Day must be between 1 and 31"):
            parse_date("2026-02-00")
    
    def test_invalid_format(self):
        """Test invalid date formats"""
        with pytest.raises(InvalidDateError, match="Date must be in format YYYY-MM-DD"):
            parse_date("02-10-2026")
        with pytest.raises(InvalidDateError, match="Date must be in format YYYY-MM-DD"):
            parse_date("2026/02/10")
        with pytest.raises(InvalidDateError, match="Date must be in format YYYY-MM-DD"):
            parse_date("not-a-date")
    
    def test_invalid_year(self):
        """Test non-numeric year"""
        with pytest.raises(InvalidDateError):
            parse_date("abcd-02-10")


class TestValidateAndCreateEntry:
    """Test suite for validate_and_create_entry function"""
    
    def test_valid_entry(self):
        """Test creating valid entry"""
        entry = validate_and_create_entry("John Doe", "ACM-101", 8.0, "2026-02-10")
        assert entry["consultant"] == "John Doe"
        assert entry["project"] == "ACM-101"
        assert entry["hours"] == 8.0
        assert entry["date"] == "2026-02-10"
    
    def test_empty_consultant(self):
        """Test that empty consultant name raises error"""
        with pytest.raises(TimesheetValidationError, match="Consultant name cannot be empty"):
            validate_and_create_entry("", "ACM-101", 8.0, "2026-02-10")
    
    def test_empty_project(self):
        """Test that empty project code raises error"""
        with pytest.raises(TimesheetValidationError, match="Project code cannot be empty"):
            validate_and_create_entry("John Doe", "", 8.0, "2026-02-10")
    
    def test_invalid_hours(self):
        """Test that invalid hours raise error"""
        with pytest.raises(InvalidHoursError):
            validate_and_create_entry("John Doe", "ACM-101", -5.0, "2026-02-10")
    
    def test_invalid_date(self):
        """Test that invalid date raises error"""
        with pytest.raises(InvalidDateError):
            validate_and_create_entry("John Doe", "ACM-101", 8.0, "invalid-date")
    
    def test_whitespace_only_consultant(self):
        """Test that whitespace-only consultant name raises error"""
        with pytest.raises(TimesheetValidationError, match="Consultant name cannot be empty"):
            validate_and_create_entry("   ", "ACM-101", 8.0, "2026-02-10")


class TestSafeGetNestedValue:
    """Test suite for safe_get_nested_value function"""
    
    def test_simple_key(self):
        """Test getting value with single key"""
        data = {"name": "John", "hours": 8}
        assert safe_get_nested_value(data, "name") == "John"
    
    def test_nested_keys(self):
        """Test getting nested values"""
        data = {"consultant": {"name": "John", "id": 123}}
        assert safe_get_nested_value(data, "consultant", "name") == "John"
        assert safe_get_nested_value(data, "consultant", "id") == 123
    
    def test_missing_key_with_default(self):
        """Test default value for missing keys"""
        data = {"name": "John"}
        assert safe_get_nested_value(data, "email", default="N/A") == "N/A"
    
    def test_missing_nested_key(self):
        """Test default for missing nested key"""
        data = {"consultant": {"name": "John"}}
        assert safe_get_nested_value(data, "consultant", "email", default="N/A") == "N/A"
    
    def test_missing_key_none_default(self):
        """Test None as default value"""
        data = {"name": "John"}
        result = safe_get_nested_value(data, "email")
        assert result is None
    
    def test_deep_nesting(self):
        """Test deeply nested values"""
        data = {"a": {"b": {"c": {"d": "value"}}}}
        assert safe_get_nested_value(data, "a", "b", "c", "d") == "value"
    
    def test_broken_chain(self):
        """Test when intermediate key doesn't exist"""
        data = {"a": {"b": "value"}}
        assert safe_get_nested_value(data, "a", "x", "y", default="N/A") == "N/A"


class TestProcessTimesheetBatch:
    """Test suite for process_timesheet_batch function"""
    
    def test_all_valid_entries(self):
        """Test batch with all valid entries"""
        entries = [
            {"consultant": "John", "project": "ACM-101", "hours": 8.0, "date": "2026-02-10"},
            {"consultant": "Jane", "project": "BET-5", "hours": 7.0, "date": "2026-02-11"}
        ]
        valid, errors = process_timesheet_batch(entries)
        assert len(valid) == 2
        assert len(errors) == 0
    
    def test_some_invalid_entries(self):
        """Test batch with some invalid entries"""
        entries = [
            {"consultant": "John", "project": "ACM-101", "hours": 8.0, "date": "2026-02-10"},
            {"consultant": "", "project": "BET-5", "hours": 6.0, "date": "2026-02-11"},
            {"consultant": "Jane", "project": "ZET-99", "hours": 7.0, "date": "2026-02-12"}
        ]
        valid, errors = process_timesheet_batch(entries)
        assert len(valid) == 2
        assert len(errors) == 1
        assert "Consultant name cannot be empty" in errors[0]
    
    def test_all_invalid_entries(self):
        """Test batch with all invalid entries"""
        entries = [
            {"consultant": "", "project": "ACM-101", "hours": 8.0, "date": "2026-02-10"},
            {"consultant": "John", "project": "", "hours": 8.0, "date": "2026-02-11"},
            {"consultant": "Jane", "project": "BET-5", "hours": -5.0, "date": "2026-02-12"}
        ]
        valid, errors = process_timesheet_batch(entries)
        assert len(valid) == 0
        assert len(errors) == 3
    
    def test_empty_batch(self):
        """Test with empty batch"""
        valid, errors = process_timesheet_batch([])
        assert len(valid) == 0
        assert len(errors) == 0
    
    def test_various_errors(self):
        """Test that different error types are captured"""
        entries = [
            {"consultant": "John", "project": "ACM-101", "hours": 30.0, "date": "2026-02-10"},
            {"consultant": "Jane", "project": "BET-5", "hours": 8.0, "date": "invalid"},
        ]
        valid, errors = process_timesheet_batch(entries)
        assert len(valid) == 0
        assert len(errors) == 2


class TestCalculateWithFallback:
    """Test suite for calculate_with_fallback function"""
    
    def test_valid_rate(self):
        """Test calculation with valid rate"""
        assert calculate_with_fallback(8.0, 75.0) == 600.0
        assert calculate_with_fallback(10.0, 50.0) == 500.0
    
    def test_zero_rate(self):
        """Test fallback with zero rate"""
        assert calculate_with_fallback(8.0, 0.0) == 400.0
    
    def test_negative_rate(self):
        """Test fallback with negative rate"""
        assert calculate_with_fallback(8.0, -10.0, 60.0) == 480.0
    
    def test_custom_fallback(self):
        """Test with custom fallback rate"""
        assert calculate_with_fallback(5.0, 0.0, 100.0) == 500.0
    
    def test_default_fallback(self):
        """Test default fallback rate"""
        assert calculate_with_fallback(10.0, -5.0) == 500.0


class TestGuaranteedCleanupOperation:
    """Test suite for guaranteed_cleanup_operation function"""
    
    def test_successful_operation(self):
        """Test successful operation"""
        result = guaranteed_cleanup_operation("timesheet.txt", "data")
        assert result is True
    
    def test_empty_filepath(self):
        """Test with empty filepath"""
        result = guaranteed_cleanup_operation("", "data")
        assert result is False
    
    def test_with_data(self):
        """Test with various data"""
        assert guaranteed_cleanup_operation("file.txt", "some data") is True
        assert guaranteed_cleanup_operation("file.txt", "") is True
    
    def test_whitespace_filepath(self):
        """Test with whitespace-only filepath"""
        result = guaranteed_cleanup_operation("   ", "data")
        # Should return False since strip() makes it empty
        assert result is False
