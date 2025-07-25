import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import tempfile
import os

from app.main import app
from app.database.database import get_db, Base
from app.models.models import Document, TaxReturn


# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def client():
    # Create tables
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    # Clean up
    Base.metadata.drop_all(bind=engine)


def test_root_endpoint(client):
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "tax_year" in data
    assert data["tax_year"] == "2024-25"


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_tax_brackets_endpoint(client):
    """Test tax brackets endpoint"""
    response = client.get("/api/tax-calculator/brackets")
    assert response.status_code == 200
    data = response.json()
    assert data["tax_year"] == "2024-25"
    assert "brackets" in data
    assert len(data["brackets"]) == 5  # 5 tax brackets
    assert data["medicare_levy"]["rate"] == 0.02


def test_tax_calculation(client):
    """Test basic tax calculation"""
    income_data = {
        "employment_income": 80000,
        "investment_income": 0,
        "business_income": 0
    }
    deduction_data = {
        "work_related_expenses": 2000,
        "work_from_home_deduction": 500
    }
    
    response = client.post("/api/tax-calculator/calculate", json={
        "income_data": income_data,
        "deduction_data": deduction_data
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "data" in data
    
    calc_data = data["data"]
    assert calc_data["total_income"] == 80000
    assert calc_data["total_deductions"] == 2500
    assert calc_data["taxable_income"] == 77500


def test_work_from_home_calculation(client):
    """Test work from home deduction calculation"""
    response = client.post("/api/tax-calculator/work-from-home", json={
        "hours_worked": 1000,
        "rate_per_hour": 0.70
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["hours_worked"] == 1000
    assert data["rate_per_hour"] == 0.70
    assert data["total_deduction"] == 700.0


def test_tax_estimation(client):
    """Test tax estimation endpoint"""
    response = client.post("/api/tax-calculator/estimate?taxable_income=75000")
    
    assert response.status_code == 200
    data = response.json()
    assert data["taxable_income"] == 75000
    assert "income_tax" in data
    assert "medicare_levy" in data
    assert "low_income_tax_offset" in data
    assert "estimated_total_tax" in data


def test_document_upload_invalid_file_type(client):
    """Test document upload with invalid file type"""
    # Create a temporary text file
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
        tmp.write(b"test content")
        tmp_path = tmp.name
    
    try:
        with open(tmp_path, "rb") as f:
            response = client.post(
                "/api/documents/upload",
                files={"file": ("test.txt", f, "text/plain")}
            )
        
        assert response.status_code == 400
        assert "File type not allowed" in response.json()["detail"]
    finally:
        os.unlink(tmp_path)


def test_document_list_empty(client):
    """Test listing documents when none exist"""
    response = client.get("/api/documents/")
    assert response.status_code == 200
    assert response.json() == []


if __name__ == "__main__":
    pytest.main([__file__])