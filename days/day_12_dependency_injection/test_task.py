"""
Tests for Day 12: Dependency Injection
"""

import pytest
from fastapi.testclient import TestClient
from .task import (
    app,
    get_db_session,
    PaginationParams,
    TimesheetValidator,
    DatabaseSession,
)


client = TestClient(app)


class TestAuthenticationDependencies:
    """Test authentication dependencies"""

    def test_valid_api_key(self):
        """Test with valid API key"""
        response = client.get("/me", headers={"X-API-Key": "secret-api-key-123"})
        assert response.status_code == 200

    def test_missing_api_key(self):
        """Test without API key"""
        response = client.get("/me")
        assert response.status_code in [401, 422]

    def test_invalid_api_key(self):
        """Test with invalid API key"""
        response = client.get("/me", headers={"X-API-Key": "invalid-key"})
        assert response.status_code == 401


class TestAuthorizationDependencies:
    """Test authorization (admin) dependencies"""

    def test_admin_can_create_consultant(self):
        """Test admin can create consultant"""
        response = client.post(
            "/consultants",
            json={"name": "Test", "email": "test@example.com", "hourly_rate": 75.0},
            headers={"X-API-Key": "admin-key-123"},
        )
        # Should succeed if admin
        assert response.status_code in [200, 201]

    def test_non_admin_cannot_create_consultant(self):
        """Test non-admin cannot create consultant"""
        response = client.post(
            "/consultants",
            json={"name": "Test", "email": "test@example.com", "hourly_rate": 75.0},
            headers={"X-API-Key": "user-key-123"},
        )
        assert response.status_code == 403


class TestDatabaseDependencies:
    """Test database session dependencies"""

    @pytest.mark.asyncio
    async def test_db_session_created(self):
        """Test database session is created"""
        async for db in get_db_session():
            assert isinstance(db, DatabaseSession)

    def test_endpoint_with_db_dependency(self):
        """Test endpoint using DB dependency"""
        response = client.get(
            "/consultants", headers={"X-API-Key": "secret-api-key-123"}
        )
        assert response.status_code == 200


class TestBusinessLogicDependencies:
    """Test business logic dependencies"""

    def test_validator_dependency(self):
        """Test validator dependency in endpoint"""
        response = client.post(
            "/timesheets",
            json={
                "consultant_id": 1,
                "project_id": 1,
                "hours": 8.0,
                "entry_date": "2026-02-10",
            },
            headers={"X-API-Key": "secret-api-key-123"},
        )
        # Should validate and process
        assert response.status_code in [200, 201, 400, 404]

    def test_timesheet_validator_class(self):
        """Test TimesheetValidator class"""
        db = DatabaseSession()
        validator = TimesheetValidator(db)

        assert validator.validate_hours(8.0) is not None
        assert validator.validate_hours(-5.0) is not None


class TestPaginationDependencies:
    """Test pagination dependencies"""

    def test_pagination_params(self):
        """Test PaginationParams class"""
        params = PaginationParams(skip=10, limit=50)
        assert params.skip == 10
        assert params.limit == 50

    def test_pagination_bounds(self):
        """Test pagination bounds validation"""
        params = PaginationParams(skip=-10, limit=200)
        assert params.skip >= 0
        assert params.limit <= 100

    def test_list_with_pagination(self):
        """Test listing endpoint with pagination"""
        response = client.get(
            "/consultants?skip=0&limit=10", headers={"X-API-Key": "secret-api-key-123"}
        )
        assert response.status_code == 200


class TestOptionalDependencies:
    """Test optional dependencies"""

    def test_filtered_endpoint_without_filter(self):
        """Test endpoint with optional filter - no filter provided"""
        response = client.get(
            "/timesheets/filtered", headers={"X-API-Key": "secret-api-key-123"}
        )
        assert response.status_code == 200

    def test_filtered_endpoint_with_filter(self):
        """Test endpoint with optional filter - filter provided"""
        response = client.get(
            "/timesheets/filtered?project_id=1",
            headers={"X-API-Key": "secret-api-key-123"},
        )
        assert response.status_code == 200


class TestDependencyChaining:
    """Test chained dependencies"""

    def test_multi_level_dependencies(self):
        """Test endpoint with multiple dependency levels"""
        # create_timesheet has: validator -> db, current_user -> api_key, db
        response = client.post(
            "/timesheets",
            json={
                "consultant_id": 1,
                "project_id": 1,
                "hours": 8.0,
                "entry_date": "2026-02-10",
            },
            headers={"X-API-Key": "secret-api-key-123"},
        )
        # All dependencies should resolve
        assert response.status_code in [200, 201, 400, 404]
