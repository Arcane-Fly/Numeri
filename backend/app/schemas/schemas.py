from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel


class DocumentBase(BaseModel):
    filename: str
    content_type: str


class DocumentCreate(DocumentBase):
    pass


class DocumentResponse(DocumentBase):
    id: int
    original_filename: str
    file_size: int
    status: str
    document_type: Optional[str] = None
    ocr_text: Optional[str] = None
    extracted_data: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    processed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class TaxReturnBase(BaseModel):
    tax_year: str = "2024-25"


class TaxReturnCreate(TaxReturnBase):
    pass


class TaxReturnUpdate(BaseModel):
    total_income: Optional[float] = None
    employment_income: Optional[float] = None
    investment_income: Optional[float] = None
    business_income: Optional[float] = None
    total_deductions: Optional[float] = None
    work_related_expenses: Optional[float] = None
    work_from_home_deduction: Optional[float] = None


class TaxReturnResponse(TaxReturnBase):
    id: int
    
    # Income
    total_income: float
    employment_income: float
    investment_income: float
    business_income: float
    
    # Deductions
    total_deductions: float
    work_related_expenses: float
    work_from_home_deduction: float
    
    # Tax calculations
    taxable_income: float
    income_tax: float
    medicare_levy: float
    
    # Offsets
    low_income_tax_offset: float
    small_business_offset: float
    
    # Final calculations
    total_tax: float
    tax_paid: float
    refund_or_amount_owed: float
    
    # Status
    is_completed: bool
    
    # Timestamps
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class WorkFromHomeCalculation(BaseModel):
    hours_worked: float
    rate_per_hour: float = 0.70  # 2024-25 ATO rate
    
    
class WorkFromHomeResponse(BaseModel):
    hours_worked: float
    rate_per_hour: float
    total_deduction: float