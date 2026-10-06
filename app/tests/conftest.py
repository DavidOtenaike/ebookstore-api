import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database.database import Base, get_db
from app.models.user import User, Author, Category

import sqlite3
from decimal import Decimal

sqlite3.register_adapter(Decimal, lambda d: str(d))

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown_db():
    
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def registered_user(client):
    client.post("/register", json={"email": "test@example.com", "password": "testpass123"})
    response = client.post("/login", json={"email": "test@example.com", "password": "testpass123"})
    token = response.json()["access_token"]
    return {"token": token, "headers": {"Authorization": f"Bearer {token}"}}


@pytest.fixture
def second_user(client):
    client.post("/register", json={"email": "second@example.com", "password": "testpass123"})
    response = client.post("/login", json={"email": "second@example.com", "password": "testpass123"})
    token = response.json()["access_token"]
    return {"token": token, "headers": {"Authorization": f"Bearer {token}"}}


@pytest.fixture
def admin_user(client):
    client.post("/register", json={"email": "admin@example.com", "password": "adminpass123"})
    response = client.post("/login", json={"email": "admin@example.com", "password": "adminpass123"})
    token = response.json()["access_token"]


    db = TestingSessionLocal()
    user = db.query(User).filter(User.email == "admin@example.com").first()
    user.role = "admin"
    db.commit()
    db.close()

    return {"token": token, "headers": {"Authorization": f"Bearer {token}"}}


@pytest.fixture
def sample_author():
    db = TestingSessionLocal()
    author = Author(name="Frank Herbert", bio="Sci-fi author")
    db.add(author)
    db.commit()
    db.refresh(author)
    author_id = author.id
    db.close()
    return author_id


@pytest.fixture
def sample_category():
    db = TestingSessionLocal()
    category = Category(name="Science Fiction")
    db.add(category)
    db.commit()
    db.refresh(category)
    category_id = category.id
    db.close()
    return category_id


@pytest.fixture
def sample_book(client, admin_user, sample_author):
    response = client.post(
        "/books",
        json={
            "title": "Dune",
            "description": "Sci-fi epic",
            "price": "19.99",
            "stock_quantity": 3,
            "author_id": sample_author
        },
        headers=admin_user["headers"]
    )
    return response.json()