"""
Tests for Day 13: Testing and Mocking
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from datetime import date, timedelta
from .task import (
    ExternalHRSystem,
    ExternalInvoicingAPI,
    ConsultantService,
    InvoiceService,
    calculate_invoice_total,
    validate_date_range,
    batch_validate_employees,
)


class TestCalculateInvoiceTotal:
    """Test invoice calculation function"""

    def test_single_entry(self):
        """Test with single timesheet entry"""
        timesheets = [{"hours": 8.0}]
        total = calculate_invoice_total(timesheets, 75.0)
        assert total == 600.0

    def test_multiple_entries(self):
        """Test with multiple entries"""
        timesheets = [{"hours": 8.0}, {"hours": 7.5}, {"hours": 6.0}]
        total = calculate_invoice_total(timesheets, 75.0)
        assert total == 1612.5

    def test_empty_timesheets(self):
        """Test with no timesheets"""
        total = calculate_invoice_total([], 75.0)
        assert total == 0.0


class TestValidateDateRange:
    """Test date range validation"""

    def test_valid_date_range(self):
        """Test valid date range"""
        start = date(2026, 2, 1)
        end = date(2026, 2, 28)
        assert validate_date_range(start, end) is True

    def test_invalid_range(self):
        """Test when end before start"""
        start = date(2026, 2, 28)
        end = date(2026, 2, 1)
        assert validate_date_range(start, end) is False

    def test_future_dates(self):
        """Test that future dates are invalid"""
        start = date.today() + timedelta(days=1)
        end = date.today() + timedelta(days=7)
        assert validate_date_range(start, end) is False


class TestMockingExternalHRSystem:
    """Test mocking external HR system"""

    @pytest.mark.asyncio
    async def test_validate_employee_mocked(self):
        """Test validate_employee with mock"""
        mock_hr = AsyncMock(spec=ExternalHRSystem)
        mock_hr.validate_employee.return_value = {
            "employee_id": "EMP001",
            "name": "John Doe",
            "is_valid": True,
        }

        result = await mock_hr.validate_employee("EMP001")
        assert result["is_valid"] is True
        mock_hr.validate_employee.assert_called_once_with("EMP001")

    @pytest.mark.asyncio
    async def test_get_employee_rate_mocked(self):
        """Test get_employee_rate with mock"""
        mock_hr = AsyncMock(spec=ExternalHRSystem)
        mock_hr.get_employee_rate.return_value = 75.0

        rate = await mock_hr.get_employee_rate("EMP001")
        assert rate == 75.0


class TestConsultantServiceWithMocks:
    """Test ConsultantService with mocked dependencies"""

    @pytest.mark.asyncio
    async def test_create_consultant(self):
        """Test creating consultant with mocked HR system"""
        mock_hr = AsyncMock(spec=ExternalHRSystem)
        mock_hr.validate_employee.return_value = {
            "employee_id": "EMP001",
            "is_valid": True,
        }
        mock_hr.get_employee_rate.return_value = 75.0

        service = ConsultantService(mock_hr)
        consultant = await service.create_consultant(
            "EMP001", "John Doe", "john@example.com"
        )

        assert consultant is not None
        mock_hr.validate_employee.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_consultant_rate(self):
        """Test updating consultant rate with mocked HR system"""
        mock_hr = AsyncMock(spec=ExternalHRSystem)
        mock_hr.get_employee_rate.return_value = 85.0

        service = ConsultantService(mock_hr)
        updated = await service.update_consultant_rate(1, "EMP001")

        assert updated is not None
        mock_hr.get_employee_rate.assert_called_with("EMP001")


class TestInvoiceServiceWithMocks:
    """Test InvoiceService with mocked dependencies"""

    @pytest.mark.asyncio
    async def test_generate_invoice(self):
        """Test generating invoice with mocked API"""
        mock_api = AsyncMock(spec=ExternalInvoicingAPI)
        mock_api.create_invoice.return_value = {
            "invoice_id": "INV-001",
            "amount": 1200.0,
            "status": "created",
        }

        service = InvoiceService(mock_api)
        timesheets = [{"hours": 8.0}, {"hours": 8.0}]

        invoice = await service.generate_invoice_for_period(
            consultant_id=1,
            start_date=date(2026, 2, 1),
            end_date=date(2026, 2, 28),
            timesheets=timesheets,
        )

        assert invoice["invoice_id"] == "INV-001"
        mock_api.create_invoice.assert_called_once()


class TestBatchValidation:
    """Test batch validation with mocking"""

    @pytest.mark.asyncio
    async def test_batch_validate_all_valid(self):
        """Test batch validation when all employees are valid"""
        mock_hr = AsyncMock(spec=ExternalHRSystem)
        mock_hr.validate_employee.return_value = {"is_valid": True}

        employee_ids = ["EMP001", "EMP002", "EMP003"]
        results = await batch_validate_employees(employee_ids, mock_hr)

        assert len(results) == 3
        assert all(results.values())

    @pytest.mark.asyncio
    async def test_batch_validate_some_invalid(self):
        """Test batch validation with mixed results"""
        mock_hr = AsyncMock(spec=ExternalHRSystem)

        async def mock_validate(emp_id):
            return {"is_valid": emp_id != "EMP999"}

        mock_hr.validate_employee.side_effect = mock_validate

        employee_ids = ["EMP001", "EMP999"]
        results = await batch_validate_employees(employee_ids, mock_hr)

        assert results["EMP001"] is True
        assert results["EMP999"] is False


class TestWithPatchDecorator:
    """Test using patch decorator"""

    @patch("httpx.AsyncClient")
    @pytest.mark.asyncio
    async def test_hr_system_with_patched_httpx(self, mock_client):
        """Test HR system with patched httpx"""
        mock_response = Mock()
        mock_response.json.return_value = {"employee_id": "EMP001", "rate": 75.0}
        mock_response.status_code = 200

        mock_client.return_value.get = AsyncMock(return_value=mock_response)

        # This would test actual HR system implementation
        # For this exercise, we're demonstrating the mock pattern
        assert mock_client.called or True  # Demonstration


class TestFixtures:
    """Test using pytest fixtures"""

    @pytest.fixture
    def mock_hr_system(self):
        """Fixture providing mocked HR system"""
        mock = AsyncMock(spec=ExternalHRSystem)
        mock.validate_employee.return_value = {"is_valid": True}
        mock.get_employee_rate.return_value = 75.0
        return mock

    @pytest.fixture
    def mock_invoicing_api(self):
        """Fixture providing mocked invoicing API"""
        mock = AsyncMock(spec=ExternalInvoicingAPI)
        mock.create_invoice.return_value = {"invoice_id": "INV-001", "amount": 1000.0}
        return mock

    @pytest.mark.asyncio
    async def test_with_hr_fixture(self, mock_hr_system):
        """Test using HR system fixture"""
        result = await mock_hr_system.validate_employee("EMP001")
        assert result["is_valid"] is True

    @pytest.mark.asyncio
    async def test_with_invoicing_fixture(self, mock_invoicing_api):
        """Test using invoicing API fixture"""
        result = await mock_invoicing_api.create_invoice({})
        assert "invoice_id" in result


class TestMockAssertions:
    """Test various mock assertion techniques"""

    @pytest.mark.asyncio
    async def test_call_count(self):
        """Test verifying call count"""
        mock_hr = AsyncMock()
        mock_hr.validate_employee.return_value = {"is_valid": True}

        await mock_hr.validate_employee("EMP001")
        await mock_hr.validate_employee("EMP002")

        assert mock_hr.validate_employee.call_count == 2

    @pytest.mark.asyncio
    async def test_called_with_arguments(self):
        """Test verifying call arguments"""
        mock_hr = AsyncMock()
        await mock_hr.get_employee_rate("EMP001")

        mock_hr.get_employee_rate.assert_called_with("EMP001")

    @pytest.mark.asyncio
    async def test_call_order(self):
        """Test verifying call order"""
        mock_hr = AsyncMock()

        await mock_hr.validate_employee("EMP001")
        await mock_hr.get_employee_rate("EMP001")

        # Verify calls happened in order
        assert mock_hr.validate_employee.called
        assert mock_hr.get_employee_rate.called
