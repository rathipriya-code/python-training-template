"""
Tests for Day 08: Async Programming Basics
"""

import pytest
import asyncio
import time
from .task import (
    async_calculate_billable_hours,
    fetch_consultant_data,
    fetch_multiple_consultants,
    save_timesheet_entry,
    save_multiple_entries,
    async_generate_report,
    async_with_timeout,
    process_batch_with_rate_limit,
    async_filter_and_process,
    measure_async_performance,
)


class TestAsyncCalculateBillableHours:
    """Test suite for async_calculate_billable_hours"""

    @pytest.mark.asyncio
    async def test_basic_calculation(self):
        """Test basic async calculation"""
        result = await async_calculate_billable_hours(40.0, 75.0)
        assert result == 30.0

    @pytest.mark.asyncio
    async def test_full_billable(self):
        """Test with 100% billable"""
        result = await async_calculate_billable_hours(40.0, 100.0)
        assert result == 40.0

    @pytest.mark.asyncio
    async def test_half_billable(self):
        """Test with 50% billable"""
        result = await async_calculate_billable_hours(40.0, 50.0)
        assert result == 20.0


class TestFetchConsultantData:
    """Test suite for fetch_consultant_data"""

    @pytest.mark.asyncio
    async def test_fetch_returns_dict(self):
        """Test that fetch returns dictionary"""
        data = await fetch_consultant_data("EMP001")
        assert isinstance(data, dict)
        assert "id" in data
        assert "name" in data
        assert "rate" in data

    @pytest.mark.asyncio
    async def test_fetch_preserves_id(self):
        """Test that fetched data includes correct ID"""
        data = await fetch_consultant_data("EMP001")
        assert data["id"] == "EMP001"

    @pytest.mark.asyncio
    async def test_fetch_has_delay(self):
        """Test that fetch implements async delay"""
        start = time.time()
        await fetch_consultant_data("EMP001")
        elapsed = time.time() - start
        assert elapsed >= 0.1  # Should have at least 0.1s delay


class TestFetchMultipleConsultants:
    """Test suite for fetch_multiple_consultants"""

    @pytest.mark.asyncio
    async def test_fetch_multiple(self):
        """Test fetching multiple consultants"""
        ids = ["EMP001", "EMP002", "EMP003"]
        results = await fetch_multiple_consultants(ids)
        assert len(results) == 3
        assert all("name" in r for r in results)

    @pytest.mark.asyncio
    async def test_fetch_multiple_concurrent(self):
        """Test that fetches run concurrently"""
        ids = ["EMP001", "EMP002", "EMP003"]
        start = time.time()
        await fetch_multiple_consultants(ids)
        elapsed = time.time() - start

        # If concurrent, should take ~0.1s, not 0.3s
        assert elapsed < 0.25  # Allow some overhead

    @pytest.mark.asyncio
    async def test_fetch_empty_list(self):
        """Test with empty list"""
        results = await fetch_multiple_consultants([])
        assert results == []

    @pytest.mark.asyncio
    async def test_fetch_preserves_order(self):
        """Test that results match input order or are complete"""
        ids = ["EMP001", "EMP002"]
        results = await fetch_multiple_consultants(ids)
        result_ids = [r["id"] for r in results]
        assert set(result_ids) == set(ids)


class TestSaveTimesheetEntry:
    """Test suite for save_timesheet_entry"""

    @pytest.mark.asyncio
    async def test_save_returns_true(self):
        """Test that save returns True"""
        entry = {"consultant": "John", "hours": 8.0}
        result = await save_timesheet_entry(entry)
        assert result is True

    @pytest.mark.asyncio
    async def test_save_has_delay(self):
        """Test that save implements async delay"""
        entry = {"consultant": "John", "hours": 8.0}
        start = time.time()
        await save_timesheet_entry(entry)
        elapsed = time.time() - start
        assert elapsed >= 0.05


class TestSaveMultipleEntries:
    """Test suite for save_multiple_entries"""

    @pytest.mark.asyncio
    async def test_save_multiple(self):
        """Test saving multiple entries"""
        entries = [
            {"consultant": "John", "hours": 8.0},
            {"consultant": "Jane", "hours": 7.0},
        ]
        success, failed = await save_multiple_entries(entries)
        assert success == 2
        assert failed == 0

    @pytest.mark.asyncio
    async def test_save_multiple_concurrent(self):
        """Test that saves run concurrently"""
        entries = [{"consultant": f"Person{i}", "hours": 8.0} for i in range(3)]
        start = time.time()
        await save_multiple_entries(entries)
        elapsed = time.time() - start

        # Should take ~0.05s if concurrent, not 0.15s
        assert elapsed < 0.1

    @pytest.mark.asyncio
    async def test_save_empty_list(self):
        """Test with empty list"""
        success, failed = await save_multiple_entries([])
        assert success == 0
        assert failed == 0


class TestAsyncGenerateReport:
    """Test suite for async_generate_report"""

    @pytest.mark.asyncio
    async def test_report_structure(self):
        """Test report has correct structure"""
        ids = ["EMP001", "EMP002"]
        report = await async_generate_report(ids)

        assert "total_consultants" in report
        assert "consultant_names" in report or "names" in report
        assert "average_rate" in report or "avg_rate" in report

    @pytest.mark.asyncio
    async def test_report_total_consultants(self):
        """Test total consultants count"""
        ids = ["EMP001", "EMP002", "EMP003"]
        report = await async_generate_report(ids)
        assert report["total_consultants"] == 3

    @pytest.mark.asyncio
    async def test_report_with_empty_list(self):
        """Test report with empty list"""
        report = await async_generate_report([])
        assert report["total_consultants"] == 0


class TestAsyncWithTimeout:
    """Test suite for async_with_timeout"""

    @pytest.mark.asyncio
    async def test_successful_fetch(self):
        """Test fetch completes within timeout"""
        data = await async_with_timeout("EMP001", 1.0)
        assert "name" in data

    @pytest.mark.asyncio
    async def test_timeout_raises_error(self):
        """Test that very short timeout raises TimeoutError"""
        with pytest.raises(asyncio.TimeoutError):
            await async_with_timeout("EMP001", 0.01)

    @pytest.mark.asyncio
    async def test_timeout_default(self):
        """Test with default timeout"""
        data = await async_with_timeout("EMP001")
        assert data is not None


class TestProcessBatchWithRateLimit:
    """Test suite for process_batch_with_rate_limit"""

    @pytest.mark.asyncio
    async def test_all_entries_processed(self):
        """Test that all entries are processed"""
        entries = [{"id": i} for i in range(5)]
        results = await process_batch_with_rate_limit(entries, 2)
        assert len(results) == 5
        assert all("processed" in r for r in results)

    @pytest.mark.asyncio
    async def test_batch_processing(self):
        """Test that batching is implemented"""
        entries = [{"id": i} for i in range(6)]
        start = time.time()
        await process_batch_with_rate_limit(entries, 2)
        elapsed = time.time() - start

        # With 6 entries and batch_size=2, should have 3 batches
        # So at least 2 waits of 0.1s each
        assert elapsed >= 0.2

    @pytest.mark.asyncio
    async def test_empty_entries(self):
        """Test with empty entries list"""
        results = await process_batch_with_rate_limit([])
        assert results == []

    @pytest.mark.asyncio
    async def test_processed_flag_added(self):
        """Test that processed flag is added to entries"""
        entries = [{"id": 1, "data": "test"}]
        results = await process_batch_with_rate_limit(entries, 1)
        assert results[0]["processed"] is True
        assert results[0]["id"] == 1


class TestAsyncFilterAndProcess:
    """Test suite for async_filter_and_process"""

    @pytest.mark.asyncio
    async def test_filters_by_hours(self):
        """Test filtering by minimum hours"""
        entries = [
            {"consultant": "John", "hours": 8.0},
            {"consultant": "Jane", "hours": 4.0},
            {"consultant": "Bob", "hours": 10.0},
        ]
        results = await async_filter_and_process(entries, 6.0)
        assert len(results) == 2
        assert all(e["hours"] >= 6.0 for e in results)

    @pytest.mark.asyncio
    async def test_no_matches(self):
        """Test when no entries match filter"""
        entries = [{"consultant": "John", "hours": 4.0}]
        results = await async_filter_and_process(entries, 10.0)
        assert len(results) == 0

    @pytest.mark.asyncio
    async def test_all_match(self):
        """Test when all entries match"""
        entries = [
            {"consultant": "John", "hours": 8.0},
            {"consultant": "Jane", "hours": 9.0},
        ]
        results = await async_filter_and_process(entries, 5.0)
        assert len(results) == 2


class TestMeasureAsyncPerformance:
    """Test suite for measure_async_performance"""

    def test_returns_timing_dict(self):
        """Test that function returns timing dictionary"""
        results = measure_async_performance()
        assert "sequential_time" in results
        assert "concurrent_time" in results
        assert "speedup" in results

    def test_concurrent_is_faster(self):
        """Test that concurrent is faster than sequential"""
        results = measure_async_performance()
        assert results["concurrent_time"] < results["sequential_time"]

    def test_speedup_calculated(self):
        """Test that speedup is calculated correctly"""
        results = measure_async_performance()
        expected_speedup = results["sequential_time"] / results["concurrent_time"]
        assert abs(results["speedup"] - expected_speedup) < 0.1

    def test_speedup_greater_than_one(self):
        """Test that speedup shows improvement"""
        results = measure_async_performance()
        assert results["speedup"] > 1.0
