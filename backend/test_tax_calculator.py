import pytest
from app.core.tax_calculator import TaxCalculator


class TestTaxCalculator:
    """Test cases for the TaxCalculator class"""
    
    def test_income_tax_calculation_basic(self):
        """Test basic income tax calculation"""
        # Test tax-free threshold
        assert TaxCalculator.calculate_income_tax(15000) == 0.0
        
        # Test 19% bracket
        assert TaxCalculator.calculate_income_tax(30000) == 2242.0  # (30000-18200) * 0.19
        
        # Test multiple brackets
        tax = TaxCalculator.calculate_income_tax(60000)
        expected = (45000 - 18200) * 0.19 + (60000 - 45000) * 0.325
        assert abs(tax - expected) < 0.01
    
    def test_medicare_levy_calculation(self):
        """Test Medicare Levy calculation"""
        # Below threshold
        assert TaxCalculator.calculate_medicare_levy(20000) == 0.0
        
        # Above threshold
        assert TaxCalculator.calculate_medicare_levy(50000) == 1000.0  # 50000 * 0.02
    
    def test_low_income_tax_offset(self):
        """Test Low Income Tax Offset calculation"""
        # Full offset
        assert TaxCalculator.calculate_low_income_tax_offset(30000) == 700.0
        
        # Partial offset
        offset = TaxCalculator.calculate_low_income_tax_offset(40000)
        expected = 700 - (40000 - 37500) * 0.05
        assert abs(offset - expected) < 0.01
        
        # No offset for high income
        assert TaxCalculator.calculate_low_income_tax_offset(100000) == 0.0
    
    def test_small_business_offset(self):
        """Test Small Business Income Tax Offset"""
        # Below threshold
        assert TaxCalculator.calculate_small_business_offset(3000) == 0.0
        
        # In range
        assert TaxCalculator.calculate_small_business_offset(10000) == 800.0  # 10000 * 0.08
        
        # Maximum offset
        assert TaxCalculator.calculate_small_business_offset(30000) == 1000.0
    
    def test_work_from_home_deduction(self):
        """Test work from home deduction calculation"""
        assert TaxCalculator.calculate_work_from_home_deduction(1000) == 700.0
        assert TaxCalculator.calculate_work_from_home_deduction(500) == 350.0
        assert TaxCalculator.calculate_work_from_home_deduction(0) == 0.0
    
    def test_superannuation_guarantee(self):
        """Test Superannuation Guarantee calculation"""
        assert TaxCalculator.calculate_superannuation_guarantee(100000) == 11500.0
        assert TaxCalculator.calculate_superannuation_guarantee(50000) == 5750.0
    
    def test_complete_tax_calculation(self):
        """Test complete tax calculation with all components"""
        income_data = {
            'employment_income': 80000,
            'investment_income': 5000,
            'business_income': 15000
        }
        
        deduction_data = {
            'work_related_expenses': 3000,
            'work_from_home_deduction': 1000,
            'other_deductions': 500
        }
        
        result = TaxCalculator.calculate_total_tax(income_data, deduction_data)
        
        # Check basic calculations
        assert result['total_income'] == 100000
        assert result['total_deductions'] == 4500
        assert result['taxable_income'] == 95500
        
        # Check that all required fields are present
        required_fields = [
            'total_income', 'total_deductions', 'taxable_income',
            'income_tax', 'medicare_levy', 'low_income_tax_offset',
            'small_business_offset', 'total_tax'
        ]
        
        for field in required_fields:
            assert field in result
            assert isinstance(result[field], (int, float))
    
    def test_edge_cases(self):
        """Test edge cases"""
        # Zero income
        result = TaxCalculator.calculate_total_tax({'employment_income': 0}, {})
        assert result['total_income'] == 0
        assert result['total_tax'] == 0
        
        # Negative taxable income (should not happen but handle gracefully)
        income_data = {'employment_income': 5000}
        deduction_data = {'work_related_expenses': 10000}
        result = TaxCalculator.calculate_total_tax(income_data, deduction_data)
        assert result['taxable_income'] == 0  # Should not go negative
        assert result['total_tax'] == 0


if __name__ == "__main__":
    pytest.main([__file__])