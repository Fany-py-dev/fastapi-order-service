# Order Processing REST API

A production-ready, asynchronous REST API service for order processing and product catalog management built with FastAPI, SQLAlchemy 2.0, PostgreSQL, and Docker

## 🛠 Tech Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL + SQLAlchemy 2.0 (Async) + Alembic (Database Migrations)
- **Validation & Settings:** Pydantic v2 & Pydantic Settings
- **Authentication & Security:** OAuth2 with JWT (Access & Refresh tokens), Password Hashing via `pwdlib[bcrypt]`
- **Containerization:** Docker & Docker Compose
- **Testing Suite:** Pytest, `pytest-asyncio`, HTTPX (using isolated SQLite in-memory DB)

## 📐 Architecture & Key Features

The project follows clean, **Layered Architecture** principles:
- `app/api/` — Transport layer (API endpoints, authorization dependencies, DB session injection)
- `app/services/` — Business logic layer (atomic transactions, stock management, order validation)
- `app/models/` — Declarative SQLAlchemy ORM models
- `app/schemas/` — Pydantic v2 schemas for request validation and response serialization
- `app/core/` — Application configuration, security utilities, and JWT handling

### Core Functionality
- **Role-Based Access Control (RBAC):** Differentiated access for `Customer` and `Admin` users.
- **Transactional Order Creation:** Automatic stock availability checks, stock reservation, and total order cost calculation within a single database transaction.
- **Containerization:** Multi-container orchestration with PostgreSQL health checks and automated Alembic migrations on startup.

## 🚀 Quick Start with Docker

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Fany-py-dev/fastapi-order-service.git](https://github.com/Fany-py-dev/fastapi-order-service.git)
   cd fastapi-order-service
