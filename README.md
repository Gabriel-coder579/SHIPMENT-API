# Shipment Management API

A high-performance, asynchronous RESTful API for shipment tracking and logistics management built with **FastAPI**, **SQLModel**, and **PostgreSQL**.

## 🚀 Features

- **Asynchronous Architecture:** Built on FastAPI and SQLAlchemy `AsyncSession` using the `asyncpg` driver for non-blocking database I/O.
- **Type Safety & Validation:** End-to-end data validation powered by Pydantic v2 schemas and SQLModel.
- **Timezone-Aware Timestamps:** Built-in UTC timezone tracking (`TIMESTAMP WITH TIME ZONE`) for precision audit logs.
- **Advanced Querying:** Search and filter shipments by status, date range, content, and weight parameters.
- **Modular Architecture:** Clean separation of concerns with dedicated layers for routes, models, services, schemas, and core configuration.
- **Security & Secret Management:** Environment configuration managed dynamically via `pydantic-settings` to prevent secret leaks.

## 🛠 Tech Stack

- **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **ORM / Database Model:** [SQLModel](https://sqlmodel.tiangolo.com/) / [SQLAlchemy 2.0](https://www.sqlalchemy.org/)
- **Database:** [PostgreSQL 18](https://www.postgresql.org/)
- **Async DB Driver:** [asyncpg](https://github.com/MagicStack/asyncpg)
- **Settings Management:** [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- **Server:** [Uvicorn](https://www.uvicorn.org/)

## 📂 Project Structure

SHIPMENT-API/
├── api/                  # Route controllers / API endpoints
│   └── routes/           # Endpoint handlers (shipments, health, etc.)
├── core/                 # Core settings, security, and database engine
│   ├── config.py         # Dynamic settings loader via Pydantic
│   └── database.py       # Async engine & session dependency injection
├── models/               # SQLModel database tables
│   └── models.py         # Shipment entity and DB tables
├── schemas/              # Pydantic schemas for requests/responses
│   └── schemas.py        # Data transfer objects (DTOs)
├── services/             # Business logic and database operations
│   └── shipment.py       # Shipment service layer
├── .env.example          # Environment variable template
├── .gitignore            # Git ignore configuration
├── main.py               # FastAPI application entry point
└── README.md             # Project documentation

## ⚙️ Getting Started

### Prerequisites

- **Python 3.10+**
- **PostgreSQL 18** (or higher) installed and running locally
- **Git**

### Installation & Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Gabriel-coder579/SHIPMENT-API.git
   cd SHIPMENT-API
   ```

2. **Create and Activate a Virtual Environment**
   - **Windows (PowerShell):**

     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```

   - **Linux / macOS:**

     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   *(If `requirements.txt` is not yet created, run `pip install fastapi uvicorn[standard] sqlmodel asyncpg pydantic-settings`)*

4. **Set Up Environment Variables**
   Copy the `.env.example` template to create your local `.env` file:

   ```bash
   cp .env.example .env
   ```

   Open `.env` and configure your database credentials:

   ```env
   DATABASE_URL=postgresql+asyncpg://postgres:your_password@localhost:5432/fastship
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=your_password
   POSTGRES_DB=fastship
   POSTGRES_PORT=5432
   POSTGRES_HOST=localhost
   ```

5. **Initialize Database Tables & Run the Application**

   ```bash
   uvicorn main:app --reload
   ```

   The server will start at `http://127.0.0.1:8000`.

## 📖 API Documentation

FastAPI automatically generates interactive API documentation. Once the server is running, you can access:

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Core Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Health check endpoint |
| `POST` | `/shipments/` | Create a new shipment |
| `GET` | `/shipments/` | List all shipments (with pagination & status filter) |
| `GET` | `/shipments/{id}` | Retrieve shipment details by ID |
| `PUT` | `/shipments/{id}` | Update shipment status/details |
| `DELETE` | `/shipments/{id}` | Soft delete or purge a shipment |

## 🔒 Security & Environment Variables

Sensitive credentials are stored strictly in local `.env` files and excluded from Git tracking via `.gitignore`.

When deploying to staging or production environments (e.g., Render, Railway, AWS), set the environment variables in the provider's dashboard matching the keys outlined in `.env.example`.
