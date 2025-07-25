"""
Australian Tax Calculator for 2024-25 Financial Year
Implements current ATO tax rates, brackets, and offsets
"""

from typing import Dict, Tuple


class TaxCalculator:
    """Australian Tax Calculator for 2024-25"""
    
    # 2024-25 Tax brackets (includes Stage 3 cuts)
    TAX_BRACKETS = [
        (18200, 0.0),      # Tax-free threshold
        (45000, 0.19),     # 19% tax rate
        (120000, 0.325),   # 32.5% tax rate  
        (180000, 0.37),    # 37% tax rate
        (float('inf'), 0.45)  # 45% tax rate
    ]
    
    # Medicare Levy
    MEDICARE_LEVY_RATE = 0.02  # 2%
    MEDICARE_LEVY_THRESHOLD = 24276  # 2024-25 threshold
    
    # Low Income Tax Offset (LITO) 2024-25
    LITO_MAX_OFFSET = 700
    LITO_THRESHOLD_1 = 37500
    LITO_THRESHOLD_2 = 45000
    LITO_RATE_1 = 0.05
    LITO_RATE_2 = 0.015
    
    # Small Business Income Tax Offset
    SMALL_BUSINESS_OFFSET_MAX = 1000
    SMALL_BUSINESS_THRESHOLD = 5000
    SMALL_BUSINESS_CUTOFF = 25000
    
    # Superannuation Guarantee
    SUPER_GUARANTEE_RATE = 0.115  # 11.5% for 2024-25
    
    # Work from Home deduction
    WORK_FROM_HOME_RATE = 0.70  # 70 cents per hour
    
    # Instant Asset Write-off threshold
    INSTANT_ASSET_WRITEOFF_THRESHOLD = 20000
    
    @classmethod
    def calculate_income_tax(cls, taxable_income: float) -> float:
        """Calculate income tax based on 2024-25 tax brackets"""
        if taxable_income <= 0:
            return 0.0
            
        total_tax = 0.0
        remaining_income = taxable_income
        previous_threshold = 0
        
        for threshold, rate in cls.TAX_BRACKETS:
            if remaining_income <= 0:
                break
                
            taxable_amount = min(remaining_income, threshold - previous_threshold)
            total_tax += taxable_amount * rate
            remaining_income -= taxable_amount
            previous_threshold = threshold
            
        return round(total_tax, 2)
    
    @classmethod
    def calculate_medicare_levy(cls, taxable_income: float) -> float:
        """Calculate Medicare Levy (2% for 2024-25)"""
        if taxable_income <= cls.MEDICARE_LEVY_THRESHOLD:
            return 0.0
        return round(taxable_income * cls.MEDICARE_LEVY_RATE, 2)
    
    @classmethod
    def calculate_low_income_tax_offset(cls, taxable_income: float) -> float:
        """Calculate Low Income Tax Offset (LITO) for 2024-25"""
        if taxable_income <= cls.LITO_THRESHOLD_1:
            return cls.LITO_MAX_OFFSET
        elif taxable_income <= cls.LITO_THRESHOLD_2:
            # Reduce offset by 5 cents for every dollar over $37,500
            reduction = (taxable_income - cls.LITO_THRESHOLD_1) * cls.LITO_RATE_1
            return max(0, cls.LITO_MAX_OFFSET - reduction)
        else:
            # Further reduction by 1.5 cents for every dollar over $45,000
            reduction_1 = (cls.LITO_THRESHOLD_2 - cls.LITO_THRESHOLD_1) * cls.LITO_RATE_1
            reduction_2 = (taxable_income - cls.LITO_THRESHOLD_2) * cls.LITO_RATE_2
            total_reduction = reduction_1 + reduction_2
            return max(0, cls.LITO_MAX_OFFSET - total_reduction)
    
    @classmethod
    def calculate_small_business_offset(cls, business_income: float) -> float:
        """Calculate Small Business Income Tax Offset"""
        if business_income < cls.SMALL_BUSINESS_THRESHOLD:
            return 0.0
        elif business_income <= cls.SMALL_BUSINESS_CUTOFF:
            # 8% of business income up to $1,000 maximum
            return min(business_income * 0.08, cls.SMALL_BUSINESS_OFFSET_MAX)
        else:
            return cls.SMALL_BUSINESS_OFFSET_MAX
    
    @classmethod
    def calculate_work_from_home_deduction(cls, hours_worked: float) -> float:
        """Calculate work from home deduction (70 cents per hour method)"""
        return round(hours_worked * cls.WORK_FROM_HOME_RATE, 2)
    
    @classmethod
    def calculate_superannuation_guarantee(cls, ordinary_earnings: float) -> float:
        """Calculate Superannuation Guarantee (11.5% for 2024-25)"""
        return round(ordinary_earnings * cls.SUPER_GUARANTEE_RATE, 2)
    
    @classmethod
    def calculate_total_tax(cls, income_data: Dict[str, float], deduction_data: Dict[str, float]) -> Dict[str, float]:
        """Calculate complete tax return summary"""
        
        # Extract income components
        employment_income = income_data.get('employment_income', 0.0)
        investment_income = income_data.get('investment_income', 0.0)
        business_income = income_data.get('business_income', 0.0)
        
        total_income = employment_income + investment_income + business_income
        
        # Extract deduction components
        work_related_expenses = deduction_data.get('work_related_expenses', 0.0)
        work_from_home_deduction = deduction_data.get('work_from_home_deduction', 0.0)
        other_deductions = deduction_data.get('other_deductions', 0.0)
        
        total_deductions = work_related_expenses + work_from_home_deduction + other_deductions
        
        # Calculate taxable income
        taxable_income = max(0, total_income - total_deductions)
        
        # Calculate tax components
        income_tax = cls.calculate_income_tax(taxable_income)
        medicare_levy = cls.calculate_medicare_levy(taxable_income)
        
        # Calculate offsets
        lito = cls.calculate_low_income_tax_offset(taxable_income)
        small_business_offset = cls.calculate_small_business_offset(business_income)
        
        # Calculate total tax after offsets
        total_tax_before_offsets = income_tax + medicare_levy
        total_offsets = lito + small_business_offset
        total_tax = max(0, total_tax_before_offsets - total_offsets)
        
        return {
            'total_income': round(total_income, 2),
            'total_deductions': round(total_deductions, 2),
            'taxable_income': round(taxable_income, 2),
            'income_tax': round(income_tax, 2),
            'medicare_levy': round(medicare_levy, 2),
            'low_income_tax_offset': round(lito, 2),
            'small_business_offset': round(small_business_offset, 2),
            'total_tax': round(total_tax, 2),
            'total_tax_before_offsets': round(total_tax_before_offsets, 2),
            'total_offsets': round(total_offsets, 2)
        }