"""
Tests for Day 11: FastAPI Advanced CRUD
"""

import pytest
from fastapi.testclient import TestClient
from .task import app, Database, filter_timesheets, aggregate_hours_by_consultant


client = TestClient(app)


class TestDatabaseClass:
    """Test Database class operations"""

    def test_database_init(self, tmp_path):
        """Test database initialization"""
        db = Database(str(tmp_path))
        assert db.data_dir.exists()

    def test_create_and_get_consultant(self, tmp_path):
        """Test creating and retrieving consultant"""
        db = Database(str(tmp_path))
        consultant = {
            "name": "John Doe",
            "email": "john@example.com",
            "hourly_rate": 75.0,
        }
        created = db.create_consultant(consultant)
        assert "id" in created

        retrieved = db.get_consultant(created["id"])
        assert retrieved["name"] == "John Doe"

    def test_update_consultant(self, tmp_path):
        """Test updating consultant"""
        db = Database(str(tmp_path))
        consultant = {"name": "Jane", "email": "jane@example.com", "hourly_rate": 80.0}
        created = db.create_consultant(consultant)

        updated_data = {
            "name": "Jane Smith",
            "email": "jane@example.com",
            "hourly_rate": 85.0,
        }
        updated = db.update_consultant(created["id"], updated_data)
        assert updated["hourly_rate"] == 85.0


class TestAdvancedEndpoints:
    """Test advanced CRUD endpoints"""

    def test_search_consultants_by_name(self):
        """Test searching consultants by name"""
        response = client.get("/consultants/search?name=John")
        assert response.status_code == 200

    def test_search_consultants_by_rate_range(self):
        """Test searching by rate range"""
        response = client.get("/consultants/search?min_rate=50&max_rate=100")
        assert response.status_code == 200

    def test_consultant_timesheets(self):
        """Test getting consultant timesheets"""
        # Create consultant
        consultant = client.post(
            "/consultants",
            json={
                "name": "Test User",
                "email": "test@example.com",
                "hourly_rate": 75.0,
            },
        ).json()

        response = client.get(f"/consultants/{consultant['id']}/timesheets")
        assert response.status_code == 200


class TestTimesheetReporting:
    """Test timesheet reporting endpoints"""

    def test_generate_report(self):
        """Test generating timesheet report"""
        response = client.get("/timesheets/report")
        assert response.status_code == 200
        data = response.json()
        assert "total_hours" in data or isinstance(data, dict)

    def test_report_with_date_filter(self):
        """Test report with date filters"""
        response = client.get(
            "/timesheets/report?start_date=2026-02-01&end_date=2026-02-28"
        )
        assert response.status_code == 200

    def test_project_stats(self):
        """Test project statistics endpoint"""
        # Create project first
        project = client.post(
            "/projects",
            json={"code": "TEST-1", "client_name": "Test", "budget_hours": 100.0},
        ).json()

        response = client.get(f"/projects/{project['id']}/stats")
        assert response.status_code == 200


class TestHelperFunctions:
    """Test helper functions"""

    def test_filter_timesheets_by_consultant(self):
        """Test filtering timesheets by consultant"""
        timesheets = [
            {"id": 1, "consultant_id": 1, "hours": 8.0},
            {"id": 2, "consultant_id": 2, "hours": 7.0},
        ]
        result = filter_timesheets(timesheets, consultant_id=1)
        assert len(result) == 1
        assert result[0]["consultant_id"] == 1

    def test_aggregate_hours(self):
        """Test hours aggregation"""
        timesheets = [
            {"consultant_id": 1, "hours": 8.0},
            {"consultant_id": 1, "hours": 7.0},
            {"consultant_id": 2, "hours": 6.0},
        ]
        result = aggregate_hours_by_consultant(timesheets)
        assert result[1] == 15.0
        assert result[2] == 6.0
