# E-Book Store API

A RESTful e-book store backend built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy**. The API supports user authentication, role-based authorization, book management, purchases, reviews, filtering, pagination, and automated testing.

## Tech Stack

* **Python**
* **FastAPI**
* **PostgreSQL**
* **SQLAlchemy**
* **Alembic**
* **Pydantic**
* **JWT**
* **bcrypt**
* **Pytest**

## Features

### Authentication & Authorization

* User registration and login
* JWT-based authentication
* Password hashing with bcrypt
* Protected endpoints using FastAPI dependencies
* Role-based authorization for administrative operations

### Book Management

* Create, retrieve, update, and delete books
* Book-author and book-category relationships
* Search and filtering
* Pagination and sorting

### Purchases

* Authenticated users can purchase books
* Purchase records are stored in the database
* Users can access their purchase history
* Prevents invalid or duplicate purchase operations

### Reviews

* Authenticated users can review purchased books
* Rating validation
* Review retrieval
* Prevents users from submitting multiple reviews for the same book

### Database

* Relational database design using SQLAlchemy
* PostgreSQL database integration
* Alembic migrations for schema evolution
* Relationships between users, books, authors, categories, purchases, and reviews

### Testing

* Automated API tests using Pytest
* Authentication and authorization tests
* CRUD endpoint tests
* Purchase and review tests
* Duplicate-operation validation
* Test database setup and dependency overrides

## API Documentation

FastAPI automatically provides interactive API documentation.

Once the application is running:

* Swagger UI: `http://localhost:8000/docs`
* ReDoc: `http://localhost:8000/redoc`

## Project Structure

```text
elibrary/
│
├── app/
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   │
│   ├── database/
│   │   ├── database.py
│   │   └── models.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── books.py
│   │   ├── purchases.py
│   │   ├── reviews.py
│   │   └── users.py
│   │
│   ├── schemas/
│   │   └── ...
│   │
│   ├── services/
│   │   └── ...
│   │
│   ├── tests/
│   │   └── ...
│   │
│   └── main.py
│
├── alembic/
│   └── ...
│
├── requirements.txt
├── .gitignore
└── README.md
```

> The exact structure may vary depending on the current project organization.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ebook-store-api.git
cd ebook-store-api
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=your_postgresql_database_url
SECRET_KEY=your_secret_key
ALGORITHM=HS256
```

Do not commit your `.env` file to GitHub.

### 5. Run database migrations

```bash
alembic upgrade head
```

### 6. Start the API

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

Interactive documentation:

```text
http://localhost:8000/docs
```

## Running Tests

Run the complete test suite with:

```bash
pytest
```

The test suite covers authentication, users, books, purchases, reviews, authorization, validation, and other API behavior.

## Authentication Flow

The API uses JWT bearer authentication.

Typical flow:

```text
Register
   ↓
Login
   ↓
Receive JWT access token
   ↓
Include token in Authorization header
   ↓
Access protected endpoints
```

Example:

```http
Authorization: Bearer <access_token>
```

## Key Backend Concepts Demonstrated

This project was built to apply practical backend engineering concepts including:

* REST API design
* FastAPI routing and dependency injection
* JWT authentication
