# Numeri - Production Architecture Overview
**Technical Architecture for Production-Ready Tax Preparation Platform**

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                             │
├─────────────────────────────────────────────────────────────────┤
│  Web Browser  │  Mobile PWA  │  Desktop App  │  API Clients    │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                         CDN LAYER                               │
├─────────────────────────────────────────────────────────────────┤
│   CloudFront/Azure CDN  │  Static Assets  │  Geographic Dist.   │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      LOAD BALANCER                             │
├─────────────────────────────────────────────────────────────────┤
│   Application Load Balancer  │  SSL Termination  │  Auto Scale │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐          │
│  │   Frontend  │    │   Backend   │    │   Worker    │          │
│  │   (React)   │    │  (FastAPI)  │    │   (Celery)  │          │
│  │             │    │             │    │             │          │
│  │ - React 18  │    │ - FastAPI   │    │ - OCR Tasks │          │
│  │ - TypeScript│    │ - Pydantic  │    │ - Tax Calc  │          │
│  │ - Tailwind  │    │ - SQLAlchemy│    │ - Email     │          │
│  │ - Vite      │    │ - Alembic   │    │ - Reports   │          │
│  └─────────────┘    └─────────────┘    └─────────────┘          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                     SERVICE LAYER                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │    Auth     │  │   Storage   │  │   External  │              │
│  │   Service   │  │   Service   │  │  Services   │              │
│  │             │  │             │  │             │              │
│  │ - OAuth 2.0 │  │ - S3/Blob   │  │ - ATO APIs  │              │
│  │ - JWT Tokens│  │ - Documents │  │ - Banks API │              │
│  │ - 2FA       │  │ - Backups   │  │ - Textract  │              │
│  │ - Sessions  │  │ - Encryption│  │ - SendGrid  │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATA LAYER                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │ PostgreSQL  │  │    Redis    │  │   Search    │              │
│  │  Database   │  │    Cache    │  │  (Optional) │              │
│  │             │  │             │  │             │              │
│  │ - Primary   │  │ - Sessions  │  │ - ElasticS  │              │
│  │ - Read Rep  │  │ - Queue     │  │ - Documents │              │
│  │ - Backup    │  │ - Cache     │  │ - Full Text │              │
│  │ - Encryption│  │ - Rate Limit│  │ - Analytics │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### Frontend Architecture (React)

```typescript
src/
├── components/          # Reusable UI components
│   ├── ui/             # Base UI components (Button, Input, etc.)
│   ├── forms/          # Form components (TaxForm, DocumentUpload)
│   ├── dashboard/      # Dashboard-specific components
│   └── layout/         # Layout components (Header, Sidebar)
├── pages/              # Route-level components
│   ├── Dashboard.tsx
│   ├── TaxCalculator.tsx
│   ├── Documents.tsx
│   └── Profile.tsx
├── hooks/              # Custom React hooks
│   ├── useAuth.ts
│   ├── useDocuments.ts
│   └── useTaxCalc.ts
├── lib/                # Utilities and API client
│   ├── api.ts          # API client configuration
│   ├── auth.ts         # Authentication utilities
│   ├── utils.ts        # Helper functions
│   └── constants.ts    # Application constants
├── store/              # State management
│   ├── authStore.ts    # Authentication state
│   ├── documentsStore.ts
│   └── taxStore.ts
└── types/              # TypeScript type definitions
    ├── api.ts
    ├── auth.ts
    └── index.ts
```

### Backend Architecture (FastAPI)

```python
app/
├── api/                # API route handlers
│   ├── v1/            # API version 1
│   │   ├── auth.py    # Authentication endpoints
│   │   ├── users.py   # User management
│   │   ├── documents.py
│   │   ├── tax_calculator.py
│   │   └── tax_returns.py
│   └── dependencies.py # Shared dependencies
├── core/              # Business logic
│   ├── auth.py        # Authentication logic
│   ├── security.py    # Security utilities
│   ├── config.py      # Configuration management
│   └── exceptions.py  # Custom exceptions
├── services/          # Service layer
│   ├── document_processor.py
│   ├── tax_calculator.py
│   ├── pdf_processor.py
│   ├── ocr_service.py
│   └── email_service.py
├── models/            # Database models
│   ├── user.py
│   ├── document.py
│   ├── tax_return.py
│   └── audit_log.py
├── schemas/           # Pydantic schemas
│   ├── user.py
│   ├── document.py
│   ├── tax_calculation.py
│   └── responses.py
├── database/          # Database configuration
│   ├── base.py
│   ├── session.py
│   └── migrations/    # Alembic migrations
├── utils/             # Utility functions
│   ├── encryption.py
│   ├── validators.py
│   └── helpers.py
└── tests/             # Test suite
    ├── unit/
    ├── integration/
    └── e2e/
```

## Database Schema

### Core Tables

```sql
-- Users and Authentication
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20),
    is_active BOOLEAN DEFAULT true,
    is_verified BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Documents
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size INTEGER NOT NULL,
    content_type VARCHAR(100) NOT NULL,
    document_type VARCHAR(50), -- payg, receipt, bank_statement, etc.
    status VARCHAR(20) DEFAULT 'pending', -- pending, processing, completed, error
    ocr_text TEXT,
    extracted_data JSONB,
    processing_errors TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP
);

-- Tax Returns
CREATE TABLE tax_returns (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    tax_year VARCHAR(10) NOT NULL, -- e.g., '2024-25'
    
    -- Income
    employment_income DECIMAL(12,2) DEFAULT 0,
    investment_income DECIMAL(12,2) DEFAULT 0,
    business_income DECIMAL(12,2) DEFAULT 0,
    other_income DECIMAL(12,2) DEFAULT 0,
    total_income DECIMAL(12,2) DEFAULT 0,
    
    -- Deductions
    work_related_expenses DECIMAL(12,2) DEFAULT 0,
    work_from_home_deduction DECIMAL(12,2) DEFAULT 0,
    other_deductions DECIMAL(12,2) DEFAULT 0,
    total_deductions DECIMAL(12,2) DEFAULT 0,
    
    -- Calculations
    taxable_income DECIMAL(12,2) DEFAULT 0,
    income_tax DECIMAL(12,2) DEFAULT 0,
    medicare_levy DECIMAL(12,2) DEFAULT 0,
    low_income_tax_offset DECIMAL(12,2) DEFAULT 0,
    small_business_offset DECIMAL(12,2) DEFAULT 0,
    total_tax DECIMAL(12,2) DEFAULT 0,
    tax_paid DECIMAL(12,2) DEFAULT 0,
    refund_or_amount_owed DECIMAL(12,2) DEFAULT 0,
    
    -- Status
    is_draft BOOLEAN DEFAULT true,
    is_lodged BOOLEAN DEFAULT false,
    
    -- Metadata
    calculation_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    lodged_at TIMESTAMP
);

-- Audit Logging
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50) NOT NULL,
    resource_id INTEGER,
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Security Architecture

### Authentication & Authorization Flow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Client    │    │   Gateway   │    │   Auth      │
│             │    │             │    │   Service   │
└─────────────┘    └─────────────┘    └─────────────┘
        │                  │                  │
        │  1. Login        │                  │
        ├─────────────────▶│                  │
        │                  │  2. Validate     │
        │                  ├─────────────────▶│
        │                  │                  │
        │                  │  3. JWT Token    │
        │                  │◀─────────────────┤
        │  4. Token        │                  │
        │◀─────────────────┤                  │
        │                  │                  │
        │  5. API Request  │                  │
        ├─────────────────▶│                  │
        │  + JWT Token     │  6. Verify Token │
        │                  ├─────────────────▶│
        │                  │                  │
        │                  │  7. User Info    │
        │                  │◀─────────────────┤
        │  8. Response     │                  │
        │◀─────────────────┤                  │
```

### Data Encryption Strategy

```yaml
Encryption at Rest:
  - Database: AES-256 encryption for sensitive columns
  - File Storage: S3 SSE-KMS or Azure Storage encryption
  - Backups: Encrypted backups with separate keys
  - Key Management: AWS KMS / Azure Key Vault

Encryption in Transit:
  - TLS 1.3 for all HTTPS connections
  - Certificate pinning for mobile apps
  - VPN for internal service communication
  - Encrypted database connections

Application Level:
  - PII field-level encryption
  - Document content encryption
  - Audit log encryption
  - Session data encryption
```

## Deployment Architecture

### Kubernetes Cluster Setup

```yaml
# Production Cluster Configuration
apiVersion: v1
kind: Namespace
metadata:
  name: numeri-prod

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: numeri-backend
  namespace: numeri-prod
spec:
  replicas: 3
  selector:
    matchLabels:
      app: numeri-backend
  template:
    metadata:
      labels:
        app: numeri-backend
    spec:
      containers:
      - name: backend
        image: numeri/backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: numeri-secrets
              key: database-url
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: numeri-frontend
  namespace: numeri-prod
spec:
  replicas: 2
  selector:
    matchLabels:
      app: numeri-frontend
  template:
    metadata:
      labels:
        app: numeri-frontend
    spec:
      containers:
      - name: frontend
        image: numeri/frontend:latest
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "200m"
```

### CI/CD Pipeline

```yaml
# GitHub Actions Workflow
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Backend Tests
        run: |
          cd backend
          pip install -r requirements.txt
          pytest --cov=app --cov-report=xml
      - name: Run Frontend Tests
        run: |
          cd frontend
          npm install
          npm run test:coverage

  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Snyk Security Scan
        uses: snyk/actions/python@master
        with:
          args: --severity-threshold=high

  build-and-deploy:
    needs: [test, security-scan]
    runs-on: ubuntu-latest
    steps:
      - name: Build Backend
        run: docker build -t numeri/backend:${{ github.sha }} ./backend
      - name: Build Frontend
        run: docker build -t numeri/frontend:${{ github.sha }} ./frontend
      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/numeri-backend backend=numeri/backend:${{ github.sha }}
          kubectl set image deployment/numeri-frontend frontend=numeri/frontend:${{ github.sha }}
```

## Monitoring & Observability

### Application Monitoring Stack

```yaml
Metrics Collection:
  - Prometheus for metrics scraping
  - Grafana for visualization
  - Custom business metrics (tax calculations, document processing)
  - Infrastructure metrics (CPU, memory, disk, network)

Logging:
  - Structured JSON logging
  - ELK Stack (Elasticsearch, Logstash, Kibana)
  - Log aggregation from all services
  - Real-time log analysis and alerting

Error Tracking:
  - Sentry for application errors
  - Real-time error notifications
  - Error trending and analysis
  - Performance transaction tracking

Health Checks:
  - Kubernetes liveness/readiness probes
  - Database connection health
  - External service health checks
  - Custom business logic health checks
```

### Performance Monitoring

```python
# Example performance monitoring middleware
from fastapi import Request
import time
import logging

@app.middleware("http")
async def performance_monitoring(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    # Log performance metrics
    logging.info({
        "method": request.method,
        "url": str(request.url),
        "status_code": response.status_code,
        "process_time": process_time,
        "user_id": getattr(request.state, "user_id", None)
    })
    
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

## Disaster Recovery & Business Continuity

### Backup Strategy

```yaml
Database Backups:
  - Automated daily full backups
  - Point-in-time recovery capability
  - Cross-region backup replication
  - 7-year retention for tax records
  - Monthly backup restoration testing

File Storage Backups:
  - Real-time replication to secondary region
  - Version control for document updates
  - Automated backup verification
  - Disaster recovery procedures

Application State:
  - Configuration backup and versioning
  - Infrastructure as Code (Terraform)
  - Automated environment recreation
  - Blue-green deployment capability
```

### Failover Procedures

```yaml
Automatic Failover:
  - Multi-AZ database deployment
  - Application load balancer health checks
  - Auto-scaling based on demand
  - Circuit breaker patterns for external services

Manual Failover:
  - Secondary region activation procedures
  - DNS failover configuration
  - Communication plan for users
  - Business continuity team activation
```

This technical architecture provides a robust, scalable, and secure foundation for the Numeri tax preparation platform, ensuring it can handle the demands of Australian tax season while maintaining compliance with all regulatory requirements.