"""
Day 10: FastAPI Basics
=======================

Theme: Consulting Timesheet Tracker - First API Endpoints

Learning Objectives:
- Create FastAPI application
- Define routes with path and query parameters
- Use Pydantic models for request/response
- Implement basic CRUD endpoints
- Handle HTTP status codes

Business Context:
Build your first FastAPI endpoints for the timesheet tracker API.
"""

from fastapi import FastAPI, HTTPException, status, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

# In-memory storage for demonstration
consultants_db = {}
projects_db = {}
timesheets_db = {}


# TODO: Import your Pydantic models from Day 09 or recreate minimal versions


app = FastAPI(
    title="Timesheet Tracker API",
    description="Consulting Timesheet Management System",
    version="1.0.0",
)


@app.get("/")
async def root():
    """
    Root endpoint - returns API information.

    Returns:
        Dictionary with API name and version
    """
    pass


@app.get("/health")
async def health_check():
    """
    Health check endpoint.

    Returns:
        Dictionary with status="healthy"
    """
    pass


@app.post("/consultants", status_code=status.HTTP_201_CREATED)
async def create_consultant(consultant: dict):
    """
    Create a new consultant.

    Args:
        consultant: Consultant data (name, employee_id, hourly_rate, email)

    Returns:
        Created consultant with generated ID

    Raises:
        HTTPException 400: If consultant data is invalid
    """
    pass


@app.get("/consultants")
async def list_consultants(
    skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=100)
):
    """
    List all consultants with pagination.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List of consultants
    """
    pass


@app.get("/consultants/{consultant_id}")
async def get_consultant(consultant_id: int):
    """
    Get a specific consultant by ID.

    Args:
        consultant_id: Consultant ID

    Returns:
        Consultant data

    Raises:
        HTTPException 404: If consultant not found
    """
    pass


@app.put("/consultants/{consultant_id}")
async def update_consultant(consultant_id: int, consultant: dict):
    """
    Update a consultant.

    Args:
        consultant_id: Consultant ID
        consultant: Updated consultant data

    Returns:
        Updated consultant

    Raises:
        HTTPException 404: If consultant not found
    """
    pass


@app.delete("/consultants/{consultant_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_consultant(consultant_id: int):
    """
    Delete a consultant.

    Args:
        consultant_id: Consultant ID

    Raises:
        HTTPException 404: If consultant not found
    """
    pass


@app.post("/projects", status_code=status.HTTP_201_CREATED)
async def create_project(project: dict):
    """
    Create a new project.

    Args:
        project: Project data (code, client_name, budget_hours, status)

    Returns:
        Created project with generated ID
    """
    pass


@app.get("/projects")
async def list_projects(
    status_filter: Optional[str] = None, skip: int = 0, limit: int = 100
):
    """
    List projects with optional status filter.

    Args:
        status_filter: Optional status to filter by
        skip: Number of records to skip
        limit: Maximum records to return

    Returns:
        List of projects
    """
    pass


@app.get("/projects/{project_id}")
async def get_project(project_id: int):
    """
    Get a specific project by ID.

    Args:
        project_id: Project ID

    Returns:
        Project data

    Raises:
        HTTPException 404: If project not found
    """
    pass


@app.post("/timesheets", status_code=status.HTTP_201_CREATED)
async def create_timesheet_entry(entry: dict):
    """
    Create a new timesheet entry.

    Args:
        entry: Timesheet entry data

    Returns:
        Created entry with generated ID

    Raises:
        HTTPException 400: If validation fails
        HTTPException 404: If consultant or project not found
    """
    pass


@app.get("/timesheets")
async def list_timesheet_entries(
    consultant_id: Optional[int] = None,
    project_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    skip: int = 0,
    limit: int = 100,
):
    """
    List timesheet entries with optional filters.

    Args:
        consultant_id: Filter by consultant
        project_id: Filter by project
        start_date: Filter by start date (inclusive)
        end_date: Filter by end date (inclusive)
        skip: Number of records to skip
        limit: Maximum records to return

    Returns:
        List of timesheet entries
    """
    pass


@app.get("/timesheets/{entry_id}")
async def get_timesheet_entry(entry_id: int):
    """
    Get a specific timesheet entry.

    Args:
        entry_id: Entry ID

    Returns:
        Timesheet entry data

    Raises:
        HTTPException 404: If entry not found
    """
    pass


@app.get("/stats/summary")
async def get_summary_stats():
    """
    Get summary statistics.

    Returns:
        Dictionary with:
        - total_consultants
        - total_projects
        - total_entries
        - total_hours
    """
    pass


@app.get("/consultants/{consultant_id}/hours")
async def get_consultant_hours(
    consultant_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
):
    """
    Get total hours for a consultant.

    Args:
        consultant_id: Consultant ID
        start_date: Optional start date filter
        end_date: Optional end date filter

    Returns:
        Dictionary with consultant info and total hours

    Raises:
        HTTPException 404: If consultant not found
    """
    pass
