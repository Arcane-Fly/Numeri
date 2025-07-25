from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Boolean, JSON
from sqlalchemy.sql import func
from enum import Enum as PyEnum

from ..database.database import Base


class DocumentStatus(PyEnum):
    PENDING = "pending"
    PROCESSING = "processing" 
    COMPLETED = "completed"
    ERROR = "error"


class DocumentType(PyEnum):
    PAYG_SUMMARY = "payg_summary"
    RECEIPT = "receipt"
    BANK_STATEMENT = "bank_statement"
    INVOICE = "invoice"
    OTHER = "other"


class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    content_type = Column(String, nullable=False)
    
    # Processing status
    status = Column(String, default=DocumentStatus.PENDING.value)
    document_type = Column(String, nullable=True)
    
    # OCR and extracted data
    ocr_text = Column(Text, nullable=True)
    extracted_data = Column(JSON, nullable=True)  # Structured data from document
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    processed_at = Column(DateTime(timezone=True), nullable=True)


class TaxReturn(Base):
    __tablename__ = "tax_returns"
    
    id = Column(Integer, primary_key=True, index=True)
    tax_year = Column(String, default="2024-25")
    
    # Income
    total_income = Column(Float, default=0.0)
    employment_income = Column(Float, default=0.0)
    investment_income = Column(Float, default=0.0)
    business_income = Column(Float, default=0.0)
    
    # Deductions
    total_deductions = Column(Float, default=0.0)
    work_related_expenses = Column(Float, default=0.0)
    work_from_home_deduction = Column(Float, default=0.0)
    
    # Tax calculations
    taxable_income = Column(Float, default=0.0)
    income_tax = Column(Float, default=0.0)
    medicare_levy = Column(Float, default=0.0)
    
    # Offsets
    low_income_tax_offset = Column(Float, default=0.0)
    small_business_offset = Column(Float, default=0.0)
    
    # Final calculations
    total_tax = Column(Float, default=0.0)
    tax_paid = Column(Float, default=0.0)
    refund_or_amount_owed = Column(Float, default=0.0)
    
    # Status
    is_completed = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())