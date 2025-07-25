export interface Document {
  id: number;
  filename: string;
  original_filename: string;
  file_size: number;
  content_type: string;
  status: 'pending' | 'processing' | 'completed' | 'error';
  document_type?: string;
  ocr_text?: string;
  extracted_data?: Record<string, any>;
  created_at: string;
  updated_at?: string;
  processed_at?: string;
}

export interface TaxReturn {
  id: number;
  tax_year: string;
  
  // Income
  total_income: number;
  employment_income: number;
  investment_income: number;
  business_income: number;
  
  // Deductions
  total_deductions: number;
  work_related_expenses: number;
  work_from_home_deduction: number;
  
  // Tax calculations
  taxable_income: number;
  income_tax: number;
  medicare_levy: number;
  
  // Offsets
  low_income_tax_offset: number;
  small_business_offset: number;
  
  // Final calculations
  total_tax: number;
  tax_paid: number;
  refund_or_amount_owed: number;
  
  // Status
  is_completed: boolean;
  
  // Timestamps
  created_at: string;
  updated_at?: string;
}

export interface TaxCalculation {
  total_income: number;
  total_deductions: number;
  taxable_income: number;
  income_tax: number;
  medicare_levy: number;
  low_income_tax_offset: number;
  small_business_offset: number;
  total_tax: number;
  total_tax_before_offsets: number;
  total_offsets: number;
}

export interface WorkFromHomeCalculation {
  hours_worked: number;
  rate_per_hour: number;
  total_deduction: number;
}

export interface TaxBracket {
  min: number;
  max: number | null;
  rate: number;
  description: string;
}

export interface TaxInfo {
  tax_year: string;
  brackets: TaxBracket[];
  medicare_levy: {
    rate: number;
    threshold: number;
  };
  lito: {
    max_offset: number;
    threshold_1: number;
    threshold_2: number;
  };
  small_business_offset: {
    max_offset: number;
    threshold: number;
    cutoff: number;
  };
  super_guarantee_rate: number;
  work_from_home_rate: number;
  instant_asset_writeoff: number;
}