from app.database.database import Base
from sqlalchemy import Column,Integer,String,Table,ForeignKey,DateTime,CheckConstraint,UniqueConstraint,Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String,unique=True,nullable=False)
    hashed_password = Column(String,nullable=False)
    role = Column(String,default="member")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    purchases = relationship("Purchase",back_populates="user")
    reviews = relationship("Review",back_populates="user")

class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True)
    name = Column(String,nullable=False)
    bio = Column(String , nullable= True)
    books = relationship("Book",back_populates="author")

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer,primary_key=True)
    name = Column(String,nullable=False)
    books = relationship("Book",secondary="book_categories",back_populates="categories")

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer,primary_key=True)
    title = Column(String,nullable=False)
    description = Column(String,nullable=False)
    price = Column(Numeric,nullable=False)
    stock_quantity = Column(Integer,nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"),nullable=False)

    author = relationship("Author",back_populates="books")
    categories = relationship("Category",secondary= "book_categories", back_populates="books")
    purchases = relationship("Purchase",back_populates="book")
    reviews = relationship("Review", back_populates="book")

class Purchase(Base):
    __tablename__ = "purchases"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    book_id = Column(Integer,ForeignKey("books.id"),nullable=False)
    purchased_at = Column(DateTime(timezone=True), server_default=func.now())
    price_at_purchase = Column(Integer)

    user = relationship("User",back_populates="purchases")
    book = relationship("Book",back_populates="purchases")

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer,primary_key=True)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    book_id = Column(Integer,ForeignKey("books.id"),nullable=False)
    rating = Column(Integer, nullable=False)
    text = Column(String,nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User",back_populates="reviews")
    book = relationship("Book",back_populates="reviews")
    __table_args__ = (
        CheckConstraint("rating >= 1 AND rating <= 5", name="check_rating_range"),
        UniqueConstraint("user_id", "book_id", name="unique_user_book_review"),
    )

book_categories = Table(
    "book_categories",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id"), primary_key=True),
    Column("category_id", Integer, ForeignKey("categories.id"), primary_key=True),
)
