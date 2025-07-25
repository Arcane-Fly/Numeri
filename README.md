# Numeri - ATO Tax Preparation Web Application

Numeri is a comprehensive Australian Tax Preparation Web Application designed for the 2024-25 financial year. It automates document processing, data extraction, and tax return preparation for individuals and small businesses.

## Features

- **Document Processing**: Upload and process tax documents (PDFs, images) with OCR
- **Automatic Classification**: Intelligent document classification (PAYG, receipts, bank statements)
- **2024-25 Tax Calculations**: Complete implementation of current ATO tax rates and rules
- **Interactive Dashboard**: Overview of document status and tax information
- **Tax Calculator**: Calculate income tax, Medicare levy, offsets, and deductions
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: SQLite (development), PostgreSQL (production)
- **Document Processing**: Tesseract OCR, pdfplumber, Pillow
- **Testing**: Pytest
- **Code Quality**: Black, Ruff

### Frontend
- **Framework**: React 18+ with TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS + shadcn/ui components
- **State Management**: React hooks
- **API Client**: Axios

### DevOps
- **Containerization**: Docker & Docker Compose
- **Web Server**: Nginx (production)
- **Development**: Hot reload for both frontend and backend

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker (optional)

### Method 1: Local Development

#### Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Method 2: Docker
```bash
docker-compose up --build
```

The application will be available at:
- Frontend: http://localhost:3000 (dev) or http://localhost:80 (Docker)
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## 2024-25 Tax Features

### Tax Brackets (Stage 3 cuts implemented)
- $0 - $18,200: 0% (Tax-free threshold)
- $18,201 - $45,000: 19%
- $45,001 - $120,000: 32.5%
- $120,001 - $180,000: 37%
- $180,001+: 45%

### Additional Features
- **Medicare Levy**: 2% (threshold: $24,276)
- **Low Income Tax Offset (LITO)**: Up to $700
- **Small Business Income Tax Offset**: Up to $1,000
- **Work from Home Deduction**: 70 cents per hour method
- **Instant Asset Write-off**: $20,000 threshold
- **Superannuation Guarantee**: 11.5%

## API Endpoints

### Documents
- `POST /api/documents/upload` - Upload and process documents
- `GET /api/documents/` - List all documents
- `GET /api/documents/{id}` - Get specific document
- `DELETE /api/documents/{id}` - Delete document

### Tax Calculator
- `POST /api/tax-calculator/calculate` - Calculate complete tax
- `POST /api/tax-calculator/work-from-home` - Calculate WFH deduction
- `GET /api/tax-calculator/brackets` - Get tax brackets and rates
- `POST /api/tax-calculator/estimate` - Quick tax estimate

### Tax Returns
- `POST /api/tax-calculator/tax-return` - Create tax return
- `GET /api/tax-calculator/tax-return/{id}` - Get tax return
- `PUT /api/tax-calculator/tax-return/{id}` - Update tax return

## Project Structure

```
numeri/
├── backend/
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── core/         # Business logic
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── database/     # Database setup
│   │   └── utils/        # Utility functions
│   ├── requirements.txt
│   ├── Dockerfile
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── lib/          # Utilities and API client
│   │   ├── types/        # TypeScript types
│   │   └── styles/       # Global styles
│   ├── package.json
│   └── Dockerfile
└── docker-compose.yml
```

## Development

### Backend Development
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest

# Format code
black .

# Lint code
ruff check .

# Run development server
uvicorn app.main:app --reload
```

### Frontend Development
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Testing

#### Backend Tests
```bash
cd backend
pytest test_*.py -v
```

#### Frontend Tests
```bash
cd frontend
npm run test
```

## Document Types Supported

- **PAYG Summary**: Automatic extraction of gross payments, tax withheld, TFN, ABN
- **Receipts/Invoices**: Extract amounts, GST, dates for deduction purposes
- **Bank Statements**: Extract account information and transaction summaries
- **Other Documents**: General OCR processing for manual review

## Tax Calculations

The application implements all current 2024-25 ATO tax rules:

1. **Income Tax**: Progressive tax brackets with Stage 3 cuts
2. **Medicare Levy**: 2% on income above threshold
3. **Offsets**: LITO and Small Business offset calculations
4. **Deductions**: Work-related expenses, WFH deductions
5. **Business Features**: Instant asset write-off, small business concessions

## Security Features

- Input validation on all API endpoints
- File type and size restrictions for uploads
- Secure file storage
- SQL injection protection via SQLAlchemy ORM
- CORS configuration for secure frontend-backend communication

## Deployment

### Production Deployment with Docker
```bash
# Build and run
docker-compose -f docker-compose.prod.yml up --build

# Run in background
docker-compose -f docker-compose.prod.yml up -d
```

### Environment Variables
Create `.env` files for configuration:

**Backend (.env)**
```
DATABASE_URL=postgresql://user:pass@localhost/numeri
SECRET_KEY=your-secret-key
DEBUG=false
CORS_ORIGINS=https://yourdomain.com
```

**Frontend (.env.production)**
```
VITE_API_BASE_URL=https://api.yourdomain.com
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Check the API documentation at `/docs` endpoint
- Review the test files for usage examples
- Open an issue on GitHub

## Roadmap

### Phase 1 (Complete)
- ✅ Core document processing
- ✅ Tax calculation engine
- ✅ Basic UI components
- ✅ API endpoints

### Phase 2 (Future)
- 🔄 User authentication
- 🔄 Data persistence per user
- 🔄 Advanced OCR improvements
- 🔄 Cloud storage integration

### Phase 3 (Future)
- 🔄 Open Banking integration
- 🔄 Accounting software sync
- 🔄 Advanced reporting
- 🔄 Multi-year support

---

**Disclaimer**: This application is designed to assist with tax preparation but should not replace professional tax advice. Always consult with a qualified tax professional for complex tax situations.