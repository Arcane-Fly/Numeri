from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any

from ..database.database import get_db
from ..models.models import TaxReturn
from ..schemas.schemas import (
    TaxReturnCreate, TaxReturnUpdate, TaxReturnResponse,
    WorkFromHomeCalculation, WorkFromHomeResponse
)
from ..core.tax_calculator import TaxCalculator

router = APIRouter()


@router.post("/calculate", response_model=Dict[str, Any])
async def calculate_tax(
    income_data: Dict[str, float],
    deduction_data: Dict[str, float] = None
):
    """Calculate tax based on income and deduction data"""
    if deduction_data is None:
        deduction_data = {}
    
    try:
        result = TaxCalculator.calculate_total_tax(income_data, deduction_data)
        return {
            "success": True,
            "data": result,
            "error": None
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Calculation failed: {str(e)}")


@router.post("/work-from-home", response_model=WorkFromHomeResponse)
async def calculate_work_from_home_deduction(
    calculation: WorkFromHomeCalculation
):
    """Calculate work from home deduction"""
    try:
        total_deduction = TaxCalculator.calculate_work_from_home_deduction(
            calculation.hours_worked
        )
        
        return WorkFromHomeResponse(
            hours_worked=calculation.hours_worked,
            rate_per_hour=calculation.rate_per_hour,
            total_deduction=total_deduction
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Calculation failed: {str(e)}")


@router.get("/brackets")
async def get_tax_brackets():
    """Get current tax brackets and rates"""
    return {
        "tax_year": "2024-25",
        "brackets": [
            {"min": 0, "max": 18200, "rate": 0.0, "description": "Tax-free threshold"},
            {"min": 18201, "max": 45000, "rate": 0.19, "description": "19% tax rate"},
            {"min": 45001, "max": 120000, "rate": 0.325, "description": "32.5% tax rate"},
            {"min": 120001, "max": 180000, "rate": 0.37, "description": "37% tax rate"},
            {"min": 180001, "max": None, "rate": 0.45, "description": "45% tax rate"}
        ],
        "medicare_levy": {
            "rate": TaxCalculator.MEDICARE_LEVY_RATE,
            "threshold": TaxCalculator.MEDICARE_LEVY_THRESHOLD
        },
        "lito": {
            "max_offset": TaxCalculator.LITO_MAX_OFFSET,
            "threshold_1": TaxCalculator.LITO_THRESHOLD_1,
            "threshold_2": TaxCalculator.LITO_THRESHOLD_2
        },
        "small_business_offset": {
            "max_offset": TaxCalculator.SMALL_BUSINESS_OFFSET_MAX,
            "threshold": TaxCalculator.SMALL_BUSINESS_THRESHOLD,
            "cutoff": TaxCalculator.SMALL_BUSINESS_CUTOFF
        },
        "super_guarantee_rate": TaxCalculator.SUPER_GUARANTEE_RATE,
        "work_from_home_rate": TaxCalculator.WORK_FROM_HOME_RATE,
        "instant_asset_writeoff": TaxCalculator.INSTANT_ASSET_WRITEOFF_THRESHOLD
    }


@router.post("/tax-return", response_model=TaxReturnResponse)
async def create_tax_return(
    tax_return: TaxReturnCreate,
    db: Session = Depends(get_db)
):
    """Create a new tax return"""
    db_tax_return = TaxReturn(**tax_return.dict())
    db.add(db_tax_return)
    db.commit()
    db.refresh(db_tax_return)
    return db_tax_return


@router.get("/tax-return/{tax_return_id}", response_model=TaxReturnResponse)
async def get_tax_return(
    tax_return_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific tax return"""
    tax_return = db.query(TaxReturn).filter(TaxReturn.id == tax_return_id).first()
    if not tax_return:
        raise HTTPException(status_code=404, detail="Tax return not found")
    return tax_return


@router.put("/tax-return/{tax_return_id}", response_model=TaxReturnResponse)
async def update_tax_return(
    tax_return_id: int,
    tax_return_update: TaxReturnUpdate,
    db: Session = Depends(get_db)
):
    """Update a tax return and recalculate"""
    tax_return = db.query(TaxReturn).filter(TaxReturn.id == tax_return_id).first()
    if not tax_return:
        raise HTTPException(status_code=404, detail="Tax return not found")
    
    # Update provided fields
    update_data = tax_return_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(tax_return, field, value)
    
    # Recalculate tax
    income_data = {
        'employment_income': tax_return.employment_income,
        'investment_income': tax_return.investment_income,
        'business_income': tax_return.business_income
    }
    
    deduction_data = {
        'work_related_expenses': tax_return.work_related_expenses,
        'work_from_home_deduction': tax_return.work_from_home_deduction
    }
    
    try:
        calculations = TaxCalculator.calculate_total_tax(income_data, deduction_data)
        
        # Update calculated fields
        tax_return.total_income = calculations['total_income']
        tax_return.total_deductions = calculations['total_deductions']
        tax_return.taxable_income = calculations['taxable_income']
        tax_return.income_tax = calculations['income_tax']
        tax_return.medicare_levy = calculations['medicare_levy']
        tax_return.low_income_tax_offset = calculations['low_income_tax_offset']
        tax_return.small_business_offset = calculations['small_business_offset']
        tax_return.total_tax = calculations['total_tax']
        
        db.commit()
        db.refresh(tax_return)
        
        return tax_return
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Calculation failed: {str(e)}")


@router.post("/estimate")
async def estimate_tax(
    taxable_income: float
):
    """Quick tax estimate for a given taxable income"""
    try:
        income_tax = TaxCalculator.calculate_income_tax(taxable_income)
        medicare_levy = TaxCalculator.calculate_medicare_levy(taxable_income)
        lito = TaxCalculator.calculate_low_income_tax_offset(taxable_income)
        
        total_tax = max(0, income_tax + medicare_levy - lito)
        
        return {
            "taxable_income": taxable_income,
            "income_tax": income_tax,
            "medicare_levy": medicare_levy,
            "low_income_tax_offset": lito,
            "estimated_total_tax": total_tax,
            "take_home_income": taxable_income - total_tax
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Estimation failed: {str(e)}")