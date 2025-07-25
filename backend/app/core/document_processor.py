"""
Document processing service for OCR and data extraction
"""

import os
import io
import re
from typing import Optional, Dict, Any, List
from PIL import Image
import pytesseract
import pdfplumber
from PyPDF2 import PdfReader

from ..models.models import DocumentType


class DocumentProcessor:
    """Service for processing uploaded documents"""
    
    def __init__(self):
        # Configure tesseract if path is provided
        from ..config import settings
        if settings.tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = settings.tesseract_cmd
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF using pdfplumber"""
        try:
            text = ""
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text.strip()
        except Exception as e:
            # Fallback to PyPDF2
            try:
                text = ""
                with open(file_path, 'rb') as file:
                    pdf_reader = PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
                return text.strip()
            except Exception:
                raise Exception(f"Failed to extract text from PDF: {str(e)}")
    
    def extract_text_from_image(self, file_path: str) -> str:
        """Extract text from image using OCR"""
        try:
            image = Image.open(file_path)
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Perform OCR
            text = pytesseract.image_to_string(image)
            return text.strip()
        except Exception as e:
            raise Exception(f"Failed to extract text from image: {str(e)}")
    
    def extract_text(self, file_path: str, content_type: str) -> str:
        """Extract text from document based on file type"""
        if content_type == "application/pdf":
            return self.extract_text_from_pdf(file_path)
        elif content_type.startswith("image/"):
            return self.extract_text_from_image(file_path)
        else:
            raise ValueError(f"Unsupported file type: {content_type}")
    
    def classify_document(self, text: str, filename: str) -> DocumentType:
        """Classify document type based on content"""
        text_lower = text.lower()
        filename_lower = filename.lower()
        
        # PAYG Summary indicators
        payg_indicators = [
            "payment summary", "payg", "group certificate", "employer",
            "gross payments", "tax withheld", "abn", "tfn"
        ]
        
        # Receipt indicators  
        receipt_indicators = [
            "receipt", "invoice", "tax invoice", "gst", "abn",
            "amount paid", "total", "purchase", "sale"
        ]
        
        # Bank statement indicators
        bank_indicators = [
            "bank statement", "account statement", "transaction",
            "balance", "deposit", "withdrawal", "interest"
        ]
        
        # Check for PAYG summary
        if any(indicator in text_lower for indicator in payg_indicators):
            return DocumentType.PAYG_SUMMARY
        
        # Check for receipt/invoice
        if any(indicator in text_lower for indicator in receipt_indicators):
            return DocumentType.RECEIPT
        
        # Check for bank statement
        if any(indicator in text_lower for indicator in bank_indicators):
            return DocumentType.BANK_STATEMENT
        
        # Check filename for hints
        if any(term in filename_lower for term in ["payg", "payment", "summary"]):
            return DocumentType.PAYG_SUMMARY
        
        if any(term in filename_lower for term in ["receipt", "invoice"]):
            return DocumentType.RECEIPT
        
        if any(term in filename_lower for term in ["statement", "bank"]):
            return DocumentType.BANK_STATEMENT
        
        return DocumentType.OTHER
    
    def extract_structured_data(self, text: str, document_type: DocumentType) -> Dict[str, Any]:
        """Extract structured data based on document type"""
        data = {}
        
        if document_type == DocumentType.PAYG_SUMMARY:
            data.update(self._extract_payg_data(text))
        elif document_type == DocumentType.RECEIPT:
            data.update(self._extract_receipt_data(text))
        elif document_type == DocumentType.BANK_STATEMENT:
            data.update(self._extract_bank_statement_data(text))
        
        return data
    
    def _extract_payg_data(self, text: str) -> Dict[str, Any]:
        """Extract data from PAYG summary"""
        data = {}
        
        # Extract gross payments
        gross_match = re.search(r'gross\s+payments?\s*:?\s*\$?([\d,]+\.?\d*)', text, re.IGNORECASE)
        if gross_match:
            amount_str = gross_match.group(1).replace(',', '')
            try:
                data['gross_payments'] = float(amount_str)
            except ValueError:
                pass
        
        # Extract tax withheld
        tax_match = re.search(r'tax\s+withheld\s*:?\s*\$?([\d,]+\.?\d*)', text, re.IGNORECASE)
        if tax_match:
            amount_str = tax_match.group(1).replace(',', '')
            try:
                data['tax_withheld'] = float(amount_str)
            except ValueError:
                pass
        
        # Extract TFN
        tfn_match = re.search(r'tfn\s*:?\s*(\d{3}\s*\d{3}\s*\d{3})', text, re.IGNORECASE)
        if tfn_match:
            data['tfn'] = tfn_match.group(1).replace(' ', '')
        
        # Extract ABN
        abn_match = re.search(r'abn\s*:?\s*(\d{2}\s*\d{3}\s*\d{3}\s*\d{3})', text, re.IGNORECASE)
        if abn_match:
            data['abn'] = abn_match.group(1).replace(' ', '')
        
        return data
    
    def _extract_receipt_data(self, text: str) -> Dict[str, Any]:
        """Extract data from receipt/invoice"""
        data = {}
        
        # Extract total amount
        total_patterns = [
            r'total\s*:?\s*\$?([\d,]+\.?\d*)',
            r'amount\s*:?\s*\$?([\d,]+\.?\d*)',
            r'grand\s+total\s*:?\s*\$?([\d,]+\.?\d*)'
        ]
        
        for pattern in total_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                amount_str = match.group(1).replace(',', '')
                try:
                    data['total_amount'] = float(amount_str)
                    break
                except ValueError:
                    continue
        
        # Extract GST
        gst_match = re.search(r'gst\s*:?\s*\$?([\d,]+\.?\d*)', text, re.IGNORECASE)
        if gst_match:
            amount_str = gst_match.group(1).replace(',', '')
            try:
                data['gst_amount'] = float(amount_str)
            except ValueError:
                pass
        
        # Extract date
        date_patterns = [
            r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            r'(\d{1,2}\s+\w+\s+\d{2,4})',
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                data['date'] = match.group(1)
                break
        
        return data
    
    def _extract_bank_statement_data(self, text: str) -> Dict[str, Any]:
        """Extract data from bank statement"""
        data = {}
        
        # Extract account number
        account_match = re.search(r'account\s+(?:number\s*:?\s*)?(\d{6,})', text, re.IGNORECASE)
        if account_match:
            data['account_number'] = account_match.group(1)
        
        # Extract statement period
        period_match = re.search(r'statement\s+period\s*:?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\s*(?:to|-)?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})', text, re.IGNORECASE)
        if period_match:
            data['period_start'] = period_match.group(1)
            data['period_end'] = period_match.group(2)
        
        # Extract balance information
        balance_patterns = [
            r'closing\s+balance\s*:?\s*\$?([\d,]+\.?\d*)',
            r'final\s+balance\s*:?\s*\$?([\d,]+\.?\d*)'
        ]
        
        for pattern in balance_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                amount_str = match.group(1).replace(',', '')
                try:
                    data['closing_balance'] = float(amount_str)
                    break
                except ValueError:
                    continue
        
        return data
    
    def process_document(self, file_path: str, content_type: str, filename: str) -> Dict[str, Any]:
        """Complete document processing pipeline"""
        try:
            # Extract text
            ocr_text = self.extract_text(file_path, content_type)
            
            # Classify document
            document_type = self.classify_document(ocr_text, filename)
            
            # Extract structured data
            extracted_data = self.extract_structured_data(ocr_text, document_type)
            
            return {
                'success': True,
                'ocr_text': ocr_text,
                'document_type': document_type.value,
                'extracted_data': extracted_data,
                'error': None
            }
            
        except Exception as e:
            return {
                'success': False,
                'ocr_text': None,
                'document_type': None,
                'extracted_data': None,
                'error': str(e)
            }