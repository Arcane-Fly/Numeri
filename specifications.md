Okay, here is the expanded project specification for "Numeri," the ATO Tax Preparation Web Application, based on your request and the provided information.

**Project Name:** Numeri - ATO Tax Preparation Web Application
**Financial Year:** 2024-25

---

### ~/.agent-os/standards/tech-stack.md

**Purpose:** Define the standard technology stack for Numeri to ensure consistency, maintainability, and scalability.

*   **Backend Framework:** Python 3.11+
    *   **Primary Framework:** FastAPI (Preferred for new features due to async capabilities and automatic API documentation, but existing Flask code acknowledged).
    *   **Secondary Option:** Flask 2.x (For maintaining existing components).
*   **Frontend Framework:** React 18+
    *   **Build Tool:** Vite 5+
    *   **Language:** TypeScript
*   **Styling:** Tailwind CSS 3.x
*   **UI Components:** shadcn/ui (built on Radix UI and Tailwind)
*   **Database:**
    *   **Default Choice (Development):** SQLite 3.x (For ease of setup and local development).
    *   **Production Choice:** PostgreSQL 15+ (For scalability, robustness, and advanced features like JSONB for document metadata).
*   **Document Processing:**
    *   **OCR Engine:** Tesseract OCR 5.x (Python `pytesseract` wrapper)
    *   **PDF Processing:** `pdfplumber` or `PyPDF2`
    *   **Image Processing:** Pillow (PIL)
*   **Authentication (Future):** OAuth 2.0 / OpenID Connect (e.g., Auth0, AWS Cognito)
*   **API Communication (Frontend):** Axios or Fetch API
*   **State Management (Frontend):** React Context API (for simple state) or Zustand/Jotai (for more complex state needs)
*   **Caching:** Redis 7.x (For caching frequently accessed data like tax rates or processed document snippets)
*   **Task Queue (Future):** Celery with Redis/RabbitMQ (For long-running tasks like complex document processing or large tax calculations)
*   **Testing:**
    *   **Backend:** Pytest
    *   **Frontend:** Vitest + React Testing Library
*   **Containerization:** Docker
*   **Orchestration (Future):** Docker Compose (Local), Kubernetes (Production)
*   **Hosting/Deployment Platform:** Manus (Current), with potential future migration to AWS/Azure/GCP for greater control.
*   **Static File Serving:** Nginx (Potentially via Manus or custom setup)
*   **CI/CD:** GitHub Actions (Preferred)

---

### ~/.agent-os/standards/code-style.md

**Purpose:** Establish consistent coding styles and conventions for Numeri to improve readability and collaboration.

*   **Indentation:**
    *   **Python:** 4 spaces (no tabs)
    *   **JavaScript/TypeScript/JSX/CSS/HTML:** 2 spaces (no tabs)
*   **Line Length:**
    *   **Python:** 88 characters (Black default)
    *   **JavaScript/TypeScript:** 100 characters
*   **Naming Conventions:**
    *   **Python:**
        *   Variables/Functions: `snake_case`
        *   Classes: `PascalCase`
        *   Constants: `UPPER_SNAKE_CASE`
        *   Modules/Packages: `snake_case`
    *   **JavaScript/TypeScript:**
        *   Variables/Functions: `camelCase`
        *   Interfaces/Types: `PascalCase` (prefixed with `I` or `T` if needed, e.g., `ITaxReturn`, `TUserData`)
        *   Classes: `PascalCase`
        *   Constants: `UPPER_SNAKE_CASE`
        *   React Components: `PascalCase`
        *   Enums: `PascalCase`
*   **File Organization:**
    *   **Backend (FastAPI/Flask):**
        *   `app/`
            *   `api/` (API routes)
            *   `core/` (Core business logic, services)
            *   `models/` (Database models)
            *   `schemas/` (Pydantic models for validation)
            *   `database/` (Database connection/session logic)
            *   `utils/` (Utility functions)
            *   `main.py` (Application entry point)
            *   `config.py` (Configuration settings)
    *   **Frontend (React/Vite):**
        *   `src/`
            *   `components/` (Reusable UI components)
            *   `pages/` (Top-level page components)
            *   `hooks/` (Custom React hooks)
            *   `lib/` (Utility functions, API clients)
            *   `types/` (TypeScript types/interfaces)
            *   `styles/` (Global styles, Tailwind config)
            *   `assets/` (Images, icons)
            *   `App.tsx` (Main App component)
            *   `main.tsx` (Entry point)
*   **Comments/Docstrings:**
    *   **Python:** Follow Google Python Style Guide for docstrings.
    *   **JavaScript/TypeScript:** Use JSDoc/TSDoc for functions, classes, and complex logic.
*   **Imports:**
    *   Group imports (Standard library, third-party, internal).
    *   Use absolute imports where possible.
    *   Sort imports alphabetically within groups (enforced by linter).
*   **Linting & Formatting:**
    *   **Python:** Black (formatter), Ruff (linter)
    *   **JavaScript/TypeScript:** Prettier (formatter), ESLint (linter)

---

### ~/.agent-os/standards/best-practices.md

**Purpose:** Define the core development principles and best practices for Numeri.

*   **Testing Philosophy:**
    *   **Write Tests:** Yes, testing is mandatory.
    *   **Approach:** Prefer a balanced approach: Unit tests for core logic (services, utilities), Integration tests for API endpoints and database interactions, Component tests for key UI elements (React Testing Library).
    *   **Coverage Goal:** Aim for >80% code coverage for critical paths (tax calculations, document processing logic).
    *   **Test Data:** Use factories/fixtures for generating test data.
*   **Performance vs. Readability:**
    *   **Default:** Prioritize code readability and maintainability.
    *   **Optimization:** Optimize only after identifying bottlenecks through profiling. Clear, well-documented code is generally preferred, even if slightly less performant, unless performance is critical (e.g., real-time OCR processing).
*   **Security Considerations:**
    *   **Data Encryption:** All sensitive data (user information, tax documents) must be encrypted at rest (database) and in transit (HTTPS/TLS 1.3).
    *   **Input Validation:** Strictly validate and sanitize all inputs (API requests, file uploads) on both frontend and backend.
    *   **Authentication/Authorization:** Implement robust user authentication (future feature) and enforce role-based access control (RBAC) where applicable.
    *   **Dependency Management:** Regularly audit and update dependencies for known vulnerabilities (e.g., using `pip-audit`, `npm audit`).
    *   **Secure Headers:** Implement appropriate HTTP security headers (X-Content-Type-Options, X-Frame-Options, etc.).
    *   **File Uploads:** Sanitize and validate uploaded files. Store them securely, potentially outside the web root. Scan for malware (future enhancement).
    *   **Compliance:** Adhere to Australian Privacy Principles (APP) under the Privacy Act 1988. Consider data residency requirements.
*   **Database Best Practices:**
    *   Use database migrations for schema changes (Alembic for SQLAlchemy).
    *   Implement database connection pooling.
    *   Use database transactions for operations that need atomicity.
    *   Index frequently queried columns.
*   **API Design:**
    *   Follow RESTful principles where applicable.
    *   Use consistent and descriptive endpoint names.
    *   Version APIs if breaking changes are introduced.
    *   Provide clear error messages and appropriate HTTP status codes.
    *   Implement rate limiting to prevent abuse.
*   **Error Handling:**
    *   Implement comprehensive error handling with centralized logging.
    *   Return user-friendly error messages in the API responses, while logging detailed errors server-side.
    *   Use appropriate HTTP status codes.
*   **Logging & Monitoring:**
    *   Implement structured logging (e.g., JSON logs) for backend services.
    *   Log significant events, errors, and user actions for auditability.
    *   Plan for application performance monitoring (APM) and error tracking (e.g., Sentry) in production.
*   **Documentation:**
    *   Maintain clear inline code documentation (docstrings, comments).
    *   Document API endpoints (Swagger/OpenAPI for FastAPI).
    *   Keep a high-level README for the project.
*   **Accessibility (a11y):**
    *   Strive for WCAG 2.1 AA compliance in the UI design and implementation.
    *   Use semantic HTML.
    *   Ensure sufficient color contrast.
    *   Provide alternative text for images.
*   **Internationalization (i18n) / Localization (l10n):**
    *   Design UI components with potential future multi-language support in mind (e.g., using translation keys).

---

### @plan-product: Numeri - ATO Tax Preparation Web Application (2024-25)

**Mission (mission.md):**
Create "Numeri," a leading, user-centric Australian tax preparation web application that simplifies and accelerates the 2024-25 tax filing process for individuals and small businesses. Numeri leverages intelligent document processing and accurate, up-to-date tax calculations to empower users, reduce stress, ensure compliance with ATO guidelines, and maximize legitimate tax savings.

**5-Phase Roadmap:**

1.  **Phase 1: Foundation & Core Processing (MVP)**
    *   Set up the standardized tech stack (FastAPI/React/PostgreSQL).
    *   Implement secure user authentication (basic login/registration).
    *   Develop core document upload functionality (PDF, images).
    *   Integrate Tesseract OCR for basic text extraction.
    *   Build initial document classification logic (e.g., PAYG, Receipt).
    *   Create basic data extraction for key fields (amounts, dates).
    *   Implement a simple, local document storage system.
    *   Develop a basic user dashboard showing uploaded documents.
    *   Set up core backend API endpoints for document handling.
    *   Implement initial project structure, linting, and testing frameworks.

2.  **Phase 2: Tax Engine & Basic Calculations**
    *   Research and implement core 2024-25 Australian tax rates and brackets for individuals .
    *   Integrate Medicare Levy calculation (2% standard rate).
    *   Implement Low Income Tax Offset (LITO) logic.
    *   Add Superannuation Guarantee calculation (11.5% rate for 2024-25) .
    *   Develop basic income and deduction processing workflows.
    *   Create API endpoints for performing these tax calculations.
    *   Build a simple tax return summary view on the frontend.
    *   Conduct unit testing on tax calculation logic.

3.  **Phase 3: Enhanced Features & User Experience**
    *   Improve OCR accuracy and handling of various document types.
    *   Refine document classification algorithms.
    *   Implement 2024-25 specific features:
        *   Work from Home deduction (70 cents per hour fixed rate method) .
        *   Instant Asset Write-off ($20,000 threshold per asset for eligible businesses) .
        *   Small Business Income Tax Offset (up to $1,000) .
    *   Add Capital Gains Tax (basic calculation logic).
    *   Enhance the user dashboard with progress tracking and key statistics.
    *   Implement document search and filtering within the user's library.
    *   Improve UI/UX based on user feedback and accessibility standards.
    *   Integrate Redis for caching tax rates and common data.

4.  **Phase 4: Integrations & Scalability**
    *   Develop integration capabilities with cloud storage services (Google Drive, Dropbox - stretch goal for MVP).
    *   Explore secure integration pathways with accounting software (Xero, MYOB - future phase).
    *   Plan for Open Banking (CDR) compliance for financial data integration (future phase).
    *   Containerize the application using Docker.
    *   Set up Docker Compose for easier local development and testing.
    *   Optimize backend performance and database queries.
    *   Implement background task processing (Celery) for long-running operations.
    *   Conduct comprehensive integration and end-to-end testing.

5.  **Phase 5: Finalization, Security & Launch**
    *   Perform rigorous security audits and penetration testing.
    *   Finalize compliance checks (Privacy Act 1988, data residency).
    *   Conduct thorough User Acceptance Testing (UAT).
    *   Optimize application for performance and scalability.
    *   Prepare production deployment strategy (CI/CD pipeline).
    *   Create user documentation and help guides.
    *   Deploy to production environment.
    *   Monitor application performance and stability post-launch.

**Technical Decisions Documented:**
*   Choice of FastAPI for new backend development (async, speed, docs).
*   Standardization on React + TypeScript + Tailwind CSS + shadcn/ui for frontend.
*   Default database choice: PostgreSQL for production, SQLite for dev.
*   Selection of Tesseract OCR for document processing.
*   Commitment to Black/Ruff (Python) and Prettier/ESLint (JS/TS) for code quality.
*   Adoption of a balanced testing approach (unit, integration, component).
*   Emphasis on security best practices (encryption, validation, auth).
*   Plan for containerization and potential cloud deployment.

**Current Status:**
An initial version of Numeri has been successfully built and deployed, demonstrating core functionalities aligned with the 2024-25 requirements (document upload, OCR, classification, basic tax calculations including Stage 3 cuts , Medicare Levy, LITO, Small Business Offset , Instant Asset Write-off , Work from Home , and Superannuation ). This provides a strong foundation for further development following the outlined roadmap and standards.
