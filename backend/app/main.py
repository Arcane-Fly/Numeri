from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from .config import settings
from .database.database import engine
from .models import Base

# Import API routers
from .api import documents, tax_calculator

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Australian Tax Preparation Web Application for 2024-25",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create upload directory if it doesn't exist
os.makedirs(settings.upload_directory, exist_ok=True)

# Mount static files
if os.path.exists(settings.upload_directory):
    app.mount("/uploads", StaticFiles(directory=settings.upload_directory), name="uploads")

# Include API routers
app.include_router(documents.router, prefix=f"{settings.api_prefix}/documents", tags=["documents"])
app.include_router(tax_calculator.router, prefix=f"{settings.api_prefix}/tax-calculator", tags=["tax-calculator"])

@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "tax_year": settings.current_tax_year,
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)