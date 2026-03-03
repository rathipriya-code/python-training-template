"""
Tests for Day 10: FastAPI Basics
"""

import pytest
from fastapi.testclient import TestClient
from datetime import date
from .task import app


client = TestClient(app)


class TestBasicEndpoints:
    """Test basic API endpoints"""

    def test_root_endpoint(self):
        """Test root endpoint returns API info"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data or "message" in data or "title" in data

    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data.get("status") == "healthy"


class TestConsultantEndpoints:
    """Test consultant CRUD endpoints"""

    def test_create_consultant(self):
        """Test creating a consultant"""
        consultant_data = {
            "name": "John Doe",
            "employee_id": "EMP001",
            "hourly_rate": 75.0,
            "email": "john@example.com",
        }
        response = client.post("/consultants", json=consultant_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "John Doe"
        assert "id" in data

    def test_list_consultants(self):
        """Test listing consultants"""
        response = client.get("/consultants")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_consultant(self):
        """Test getting specific consultant"""
        # Create a consultant first
        create_response = client.post(
            "/consultants",
            json={
                "name": "Jane Smith",
                "employee_id": "EMP002",
                "hourly_rate": 80.0,
                "email": "jane@example.com",
            },
        )
        consultant_id = create_response.json()["id"]

        # Get the consultant
        response = client.get(f"/consultants/{consultant_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Jane Smith"

    def test_get_nonexistent_consultant(self):
        """Test getting non-existent consultant returns 404"""
        response = client.get("/consultants/99999")
        assert response.status_code == 404

    def test_update_consultant(self):
        """Test updating a consultant"""
        # Create consultant
        create_response = client.post(
            "/consultants",
            json={
                "name": "Bob Johnson",
                "employee_id": "EMP003",
                "hourly_rate": 70.0,
                "email": "bob@example.com",
            },
        )
        consultant_id = create_response.json()["id"]

        # Update consultant
        update_data = {
            "name": "Bob Johnson Sr.",
            "employee_id": "EMP003",
            "hourly_rate": 85.0,
            "email": "bob@example.com",
        }
        response = client.put(f"/consultants/{consultant_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["hourly_rate"] == 85.0

    def test_delete_consultant(self):
        """Test deleting a consultant"""
        # Create consultant
        create_response = client.post(
            "/consultants",
            json={
                "name": "Delete Me",
                "employee_id": "EMP999",
                "hourly_rate": 50.0,
                "email": "delete@example.com",
            },
        )
        consultant_id = create_response.json()["id"]

        # Delete consultant
        response = client.delete(f"/consultants/{consultant_id}")
        assert response.status_code == 204

        # Verify deletion
        get_response = client.get(f"/consultants/{consultant_id}")
        assert get_response.status_code == 404


class TestProjectEndpoints:
    """Test project endpoints"""

    def test_create_project(self):
        """Test creating a project"""
        project_data = {
            "code": "ACM-101",
            "client_name": "Acme Corp",
            "budget_hours": 100.0,
            "status": "active",
        }
        response = client.post("/projects", json=project_data)
        assert response.status_code == 201
        data = response.json()
        assert data["code"] == "ACM-101"
        assert "id" in data

    def test_list_projects(self):
        """Test listing projects"""
        response = client.get("/projects")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_list_projects_with_filter(self):
        """Test listing projects with status filter"""
        response = client.get("/projects?status_filter=active")
        assert response.status_code == 200

    def test_get_project(self):
        """Test getting specific project"""
        # Create project
        create_response = client.post(
            "/projects",
            json={
                "code": "BET-5",
                "client_name": "Beta Inc",
                "budget_hours": 50.0,
                "status": "active",
            },
        )
        project_id = create_response.json()["id"]

        # Get project
        response = client.get(f"/projects/{project_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == "BET-5"


class TestTimesheetEndpoints:
    """Test timesheet entry endpoints"""

    def test_create_timesheet_entry(self):
        """Test creating a timesheet entry"""
        # Create consultant and project first
        consultant = client.post(
            "/consultants",
            json={
                "name": "Test User",
                "employee_id": "EMP100",
                "hourly_rate": 75.0,
                "email": "test@example.com",
            },
        ).json()

        project = client.post(
            "/projects",
            json={
                "code": "TEST-1",
                "client_name": "Test Client",
                "budget_hours": 100.0,
                "status": "active",
            },
        ).json()

        # Create timesheet entry
        entry_data = {
            "consultant_id": consultant["id"],
            "project_id": project["id"],
            "hours": 8.0,
            "entry_date": "2026-02-10",
            "description": "Testing",
        }
        response = client.post("/timesheets", json=entry_data)
        assert response.status_code == 201
        data = response.json()
        assert data["hours"] == 8.0

    def test_list_timesheet_entries(self):
        """Test listing timesheet entries"""
        response = client.get("/timesheets")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_list_timesheets_with_filters(self):
        """Test listing with filters"""
        response = client.get("/timesheets?skip=0&limit=10")
        assert response.status_code == 200

    def test_get_timesheet_entry(self):
        """Test getting specific timesheet entry"""
        # Setup and create entry
        consultant = client.post(
            "/consultants",
            json={
                "name": "Entry Test",
                "employee_id": "EMP200",
                "hourly_rate": 75.0,
                "email": "entry@example.com",
            },
        ).json()

        project = client.post(
            "/projects",
            json={
                "code": "ENTRY-1",
                "client_name": "Entry Client",
                "budget_hours": 100.0,
                "status": "active",
            },
        ).json()

        entry = client.post(
            "/timesheets",
            json={
                "consultant_id": consultant["id"],
                "project_id": project["id"],
                "hours": 7.5,
                "entry_date": "2026-02-10",
            },
        ).json()

        # Get entry
        response = client.get(f"/timesheets/{entry['id']}")
        assert response.status_code == 200
        data = response.json()
        assert data["hours"] == 7.5


class TestStatsEndpoints:
    """Test statistics endpoints"""

    def test_get_summary_stats(self):
        """Test getting summary statistics"""
        response = client.get("/stats/summary")
        assert response.status_code == 200
        data = response.json()
        assert "total_consultants" in data
        assert "total_projects" in data
        assert "total_entries" in data
        assert "total_hours" in data

    def test_get_consultant_hours(self):
        """Test getting consultant hours"""
        # Create consultant and entry
        consultant = client.post(
            "/consultants",
            json={
                "name": "Hours Test",
                "employee_id": "EMP300",
                "hourly_rate": 75.0,
                "email": "hours@example.com",
            },
        ).json()

        project = client.post(
            "/projects",
            json={
                "code": "HOURS-1",
                "client_name": "Hours Client",
                "budget_hours": 100.0,
                "status": "active",
            },
        ).json()

        client.post(
            "/timesheets",
            json={
                "consultant_id": consultant["id"],
                "project_id": project["id"],
                "hours": 8.0,
                "entry_date": "2026-02-10",
            },
        )

        # Get consultant hours
        response = client.get(f"/consultants/{consultant['id']}/hours")
        assert response.status_code == 200
        data = response.json()
        assert "total_hours" in data


class TestPagination:
    """Test pagination parameters"""

    def test_consultants_pagination(self):
        """Test pagination for consultants"""
        response = client.get("/consultants?skip=0&limit=5")
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 5

    def test_projects_pagination(self):
        """Test pagination for projects"""
        response = client.get("/projects?skip=0&limit=10")
        assert response.status_code == 200

    def test_timesheets_pagination(self):
        """Test pagination for timesheets"""
        response = client.get("/timesheets?skip=0&limit=20")
        assert response.status_code == 200


class TestErrorHandling:
    """Test error handling"""

    def test_invalid_consultant_id(self):
        """Test invalid consultant ID returns 404"""
        response = client.get("/consultants/99999")
        assert response.status_code == 404

    def test_invalid_project_id(self):
        """Test invalid project ID returns 404"""
        response = client.get("/projects/99999")
        assert response.status_code == 404

    def test_invalid_timesheet_id(self):
        """Test invalid timesheet ID returns 404"""
        response = client.get("/timesheets/99999")
        assert response.status_code == 404
