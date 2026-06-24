import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Fixture: Provides a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def sample_email():
    """Fixture: Provides a sample student email"""
    return "test.student@mergington.edu"


@pytest.fixture
def sample_activity():
    """Fixture: Provides a sample activity name"""
    return "Chess Club"


@pytest.fixture
def another_email():
    """Fixture: Provides another sample email"""
    return "another.student@mergington.edu"
