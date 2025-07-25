import React, { useState } from 'react';
import { Calculator } from 'lucide-react';
import { Button, Card, CardContent, CardHeader, CardTitle } from './ui';
import { taxCalculatorApi } from '../lib/api';
import { formatCurrency } from '../lib/utils';
import type { TaxCalculation } from '../types';

export const TaxCalculator: React.FC = () => {
  const [incomeData, setIncomeData] = useState({
    employment_income: 0,
    investment_income: 0,
    business_income: 0,
  });

  const [deductionData, setDeductionData] = useState({
    work_related_expenses: 0,
    work_from_home_deduction: 0,
    other_deductions: 0,
  });

  const [calculation, setCalculation] = useState<TaxCalculation | null>(null);
  const [calculating, setCalculating] = useState(false);

  const handleCalculate = async () => {
    setCalculating(true);
    try {
      const result = await taxCalculatorApi.calculate(incomeData, deductionData);
      if (result.success) {
        setCalculation(result.data);
      } else {
        alert('Calculation failed: ' + (result.error || 'Unknown error'));
      }
    } catch (error) {
      console.error('Calculation failed:', error);
      alert('Calculation failed. Please try again.');
    } finally {
      setCalculating(false);
    }
  };

  const updateIncome = (field: keyof typeof incomeData, value: string) => {
    setIncomeData(prev => ({
      ...prev,
      [field]: parseFloat(value) || 0,
    }));
  };

  const updateDeduction = (field: keyof typeof deductionData, value: string) => {
    setDeductionData(prev => ({
      ...prev,
      [field]: parseFloat(value) || 0,
    }));
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Calculator size={24} />
            <span>Tax Calculator (2024-25)</span>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Income Section */}
          <div>
            <h3 className="text-lg font-semibold mb-3">Income</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1">
                  Employment Income
                </label>
                <input
                  type="number"
                  value={incomeData.employment_income || ''}
                  onChange={(e) => updateIncome('employment_income', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="0.00"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">
                  Investment Income
                </label>
                <input
                  type="number"
                  value={incomeData.investment_income || ''}
                  onChange={(e) => updateIncome('investment_income', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="0.00"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">
                  Business Income
                </label>
                <input
                  type="number"
                  value={incomeData.business_income || ''}
                  onChange={(e) => updateIncome('business_income', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="0.00"
                />
              </div>
            </div>
          </div>

          {/* Deductions Section */}
          <div>
            <h3 className="text-lg font-semibold mb-3">Deductions</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1">
                  Work Related Expenses
                </label>
                <input
                  type="number"
                  value={deductionData.work_related_expenses || ''}
                  onChange={(e) => updateDeduction('work_related_expenses', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="0.00"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">
                  Work From Home Deduction
                </label>
                <input
                  type="number"
                  value={deductionData.work_from_home_deduction || ''}
                  onChange={(e) => updateDeduction('work_from_home_deduction', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="0.00"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">
                  Other Deductions
                </label>
                <input
                  type="number"
                  value={deductionData.other_deductions || ''}
                  onChange={(e) => updateDeduction('other_deductions', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="0.00"
                />
              </div>
            </div>
          </div>

          <Button
            onClick={handleCalculate}
            disabled={calculating}
            className="w-full md:w-auto"
          >
            {calculating ? 'Calculating...' : 'Calculate Tax'}
          </Button>
        </CardContent>
      </Card>

      {/* Results */}
      {calculation && (
        <Card>
          <CardHeader>
            <CardTitle>Tax Calculation Results</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-3">
                <h4 className="font-semibold">Income Summary</h4>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span>Total Income:</span>
                    <span className="font-medium">{formatCurrency(calculation.total_income)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Total Deductions:</span>
                    <span className="font-medium">{formatCurrency(calculation.total_deductions)}</span>
                  </div>
                  <div className="flex justify-between font-semibold border-t pt-2">
                    <span>Taxable Income:</span>
                    <span>{formatCurrency(calculation.taxable_income)}</span>
                  </div>
                </div>
              </div>

              <div className="space-y-3">
                <h4 className="font-semibold">Tax Breakdown</h4>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span>Income Tax:</span>
                    <span className="font-medium">{formatCurrency(calculation.income_tax)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Medicare Levy:</span>
                    <span className="font-medium">{formatCurrency(calculation.medicare_levy)}</span>
                  </div>
                  <div className="flex justify-between text-green-600">
                    <span>LITO:</span>
                    <span className="font-medium">-{formatCurrency(calculation.low_income_tax_offset)}</span>
                  </div>
                  <div className="flex justify-between text-green-600">
                    <span>Small Business Offset:</span>
                    <span className="font-medium">-{formatCurrency(calculation.small_business_offset)}</span>
                  </div>
                  <div className="flex justify-between font-semibold text-lg border-t pt-2">
                    <span>Total Tax:</span>
                    <span>{formatCurrency(calculation.total_tax)}</span>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};