"""
Tests for Day 01: Type Hinting and Basic Functions
"""

from .task import (
    calculate_billable_hours,
    format_consultant_name,
    calculate_hourly_rate,
    is_overtime,
    get_project_code,
)


class TestCalculateBillableHours:
    """Test suite for calculate_billable_hours function"""

    def test_standard_calculation(self):
        """Test standard billable hours calculation"""
        assert calculate_billable_hours(40.0, 75.0) == 30.0
        assert calculate_billable_hours(35.5, 50.0) == 17.75

    def test_full_billable(self):
        """Test when all hours are billable"""
        assert calculate_billable_hours(40.0, 100.0) == 40.0
        assert calculate_billable_hours(37.5, 100.0) == 37.5

    def test_non_billable(self):
        """Test when no hours are billable"""
        assert calculate_billable_hours(40.0, 0.0) == 0.0

    def test_partial_billable(self):
        """Test various billable percentages"""
        assert calculate_billable_hours(40.0, 25.0) == 10.0
        assert calculate_billable_hours(20.0, 80.0) == 16.0

    def test_decimal_hours(self):
        """Test with decimal precision"""
        result = calculate_billable_hours(42.75, 60.0)
        assert result == 25.65


class TestFormatConsultantName:
    """Test suite for format_consultant_name function"""

    def test_basic_formatting(self):
        """Test basic name formatting"""
        assert format_consultant_name("John", "Doe") == "John Doe"
        assert format_consultant_name("Jane", "Smith") == "Jane Smith"

    def test_with_title(self):
        """Test name formatting with title"""
        assert format_consultant_name("John", "Doe", True) == "Consultant John Doe"
        assert (
            format_consultant_name("Jane", "Smith", include_title=True)
            == "Consultant Jane Smith"
        )

    def test_without_title_explicit(self):
        """Test explicitly setting include_title to False"""
        assert format_consultant_name("Bob", "Johnson", False) == "Bob Johnson"

    def test_single_letter_names(self):
        """Test with single letter names"""
        assert format_consultant_name("A", "B") == "A B"

    def test_hyphenated_names(self):
        """Test with hyphenated names"""
        assert (
            format_consultant_name("Mary-Jane", "Watson-Parker")
            == "Mary-Jane Watson-Parker"
        )


class TestCalculateHourlyRate:
    """Test suite for calculate_hourly_rate function"""

    def test_standard_calculation(self):
        """Test standard hourly rate calculation (40 hours/week)"""
        assert calculate_hourly_rate(104000, 40) == 50.0
        assert calculate_hourly_rate(78000, 40) == 37.5

    def test_default_working_hours(self):
        """Test using default working hours parameter"""
        assert calculate_hourly_rate(104000) == 50.0
        assert calculate_hourly_rate(52000) == 25.0

    def test_part_time_hours(self):
        """Test with part-time hours"""
        assert calculate_hourly_rate(52000, 20) == 50.0
        assert calculate_hourly_rate(39000, 30) == 25.0

    def test_high_salary(self):
        """Test with high salary values"""
        assert calculate_hourly_rate(208000, 40) == 100.0
        assert calculate_hourly_rate(156000, 40) == 75.0

    def test_rounding(self):
        """Test proper rounding to 2 decimal places"""
        result = calculate_hourly_rate(100000, 40)
        assert result == 48.08
        assert isinstance(result, float)


class TestIsOvertime:
    """Test suite for is_overtime function"""

    def test_overtime_worked(self):
        """Test when overtime is worked"""
        assert is_overtime(45.0) is True
        assert is_overtime(50.0) is True
        assert is_overtime(40.5) is True

    def test_no_overtime(self):
        """Test when no overtime is worked"""
        assert is_overtime(40.0) is False
        assert is_overtime(35.0) is False
        assert is_overtime(38.5) is False

    def test_custom_standard_hours(self):
        """Test with custom standard hours"""
        assert is_overtime(38.0, 35.0) is True
        assert is_overtime(37.5, 37.5) is False
        assert is_overtime(30.0, 35.0) is False

    def test_edge_cases(self):
        """Test edge cases"""
        assert is_overtime(40.0, 40.0) is False
        assert is_overtime(40.01, 40.0) is True
        assert is_overtime(0.0, 40.0) is False


class TestGetProjectCode:
    """Test suite for get_project_code function"""

    def test_with_project_id(self):
        """Test project code generation with project ID"""
        assert get_project_code("Acme Corp", 101) == "ACM-101"
        assert get_project_code("Beta Industries", 5) == "BET-5"
        assert get_project_code("Zeta Solutions", 999) == "ZET-999"

    def test_without_project_id(self):
        """Test project code generation without project ID"""
        assert get_project_code("Acme Corp") == "ACM"
        assert get_project_code("Beta Industries") == "BET"
        assert get_project_code("Zeta Solutions") == "ZET"

    def test_short_client_names(self):
        """Test with client names shorter than 3 characters"""
        assert get_project_code("XY", 5) == "XY-5"
        assert get_project_code("AB") == "AB"
        assert get_project_code("Z", 10) == "Z-10"

    def test_lowercase_conversion(self):
        """Test that lowercase names are converted to uppercase"""
        assert get_project_code("acme corp", 1) == "ACM-1"
        assert get_project_code("beta industries") == "BET"

    def test_special_characters(self):
        """Test handling of special characters in client names"""
        assert get_project_code("ABC-Corp", 50) == "ABC-50"
        assert get_project_code("XYZ & Co", 25) == "XYZ-25"
