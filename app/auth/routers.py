from fastapi import APIRouter,Depends,Query,HTTPException
from app.core.security import hash_password,verify_password,review_permitted
from app.database.database import get_db
from app.models.user import User,Book,Author,Category, Purchase,Review
from app.core.exceptions import UserAlreadyExistsException,InvalidDetailsException,UserNotFoundException,InvalidRoleException,BookNotFoundException,BookAlreadyExistsException,ReviewNotFoundException
from app.core.security import create_access_token,get_current_user,verify_user_access
from app.schemas.user import UserCreate,UserResponse,Login,BookCreate,BookResponse,SimpleCategoryResponse,BookUpdate,SimpleAuthorResponse,PaginatedBooksResponse,UserPurchaseResponse,ReviewCreate,ReviewResponse
from sqlalchemy import select,func, update

router = APIRouter()

@router.post("/register",response_model=UserResponse)
def register_user(user1:UserCreate,db = Depends(get_db)):
    user_existence = db.query(User).filter(User.email == user1.email).first()
    if user_existence is not None:
        raise UserAlreadyExistsException()
    password1 = hash_password(user1.password)
    new_user = User(
    email = user1.email,
    hashed_password = password1
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def user_login(login1:Login,db = Depends(get_db)):
    user_verify = db.query(User).filter(User.email==login1.email).first()
    if user_verify is None:
        raise InvalidDetailsException()
    password_verify = verify_password(login1.password,user_verify.hashed_password)
    if password_verify is False:
        raise InvalidDetailsException()
    data = {"sub":str(user_verify.id)}
    access_token = create_access_token(data)
    return{
        "access_token":access_token,
        "token_type":"bearer"
    }

@router.get("/me",response_model=UserResponse)
def get_profile(current_user = Depends(get_current_user)):
    return current_user

@router.patch("/users/{id}/role", dependencies=[Depends(verify_user_access)])
def change_role(id:int,role:str,db = Depends(get_db)):
    user_to_change = db.query(User).filter(User.id==id).first()
    if user_to_change is None:
        raise UserNotFoundException()
    if role not in ["admin","member"]:
        raise InvalidRoleException()
    
    user_to_change.role = role
    db.commit()
    db.refresh(user_to_change)
    return{
        "message":"Role successfully changed"
    }



@router.get("/books",response_model=PaginatedBooksResponse)
def get_book_filter(
    limit:int = Query(10, le=100, ge=1),
    page:int = Query(1, ge=1),
    author :str | None=None,
    categories :str|None = None,
    db=Depends(get_db)
    ):
    query = select(Book)
    if author is not None:
            query = query.join(Book.author).where(Author.name.ilike(f"%{author}%"))

    if categories is not None:
        query = query.join(Book.categories).where(Category.name.ilike(f"%{categories}%"))

    count_query = select(func.count()).select_from(query.subquery())
    total = db.execute(count_query).scalar()
    query = (
        query.offset((page-1)*limit)
        .limit(limit)
    )
    result = db.execute(query)
    books = result.scalars().all()
    return {
    "items": books,
    "total": total,
    "page": page,
    "limit": limit,
    "pages": (total + limit - 1) // limit if total else 0
}

@router.get("/books/{book_id}",response_model=BookResponse)
def get_book(book_id:int, db = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise BookNotFoundException()
    return book

@router.post("/books",dependencies=[Depends(verify_user_access)],response_model=BookResponse)
def create_book(book1:BookCreate,db=Depends(get_db)):
    book_check = db.query(Book).filter(Book.title==book1.title).first()
    if book_check is not None:
        raise BookAlreadyExistsException()
    new_book = Book(
        title = book1.title,
        description = book1.description,
        price = book1.price,
        stock_quantity = book1.stock_quantity,
        author_id = book1.author_id
    )

    if book1.category_ids:  
        categories = db.query(Category).filter(Category.id.in_(book1.category_ids)).all()
        new_book.categories = categories

    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@router.patch("/books/{book_id}",dependencies = [Depends(verify_user_access)],response_model=BookResponse)
def update_book(book1:BookUpdate,book_id:int,db=Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise BookNotFoundException()

    if book1.title is not None:
        book.title = book1.title
    if book1.description is not None:
        book.description = book1.description
    if book1.price is not None:
        book.price = book1.price
    if book1.stock_quantity is not None:
        book.stock_quantity = book1.stock_quantity
    if book1.author_id is not None:
        book.author_id = book1.author_id
    if book1.category_ids is not None:
        categories = db.query(Category).filter(Category.id.in_(book1.category_ids)).all()
        book.categories = categories

    db.commit()
    return book

@router.delete("/books/{book_id}", dependencies=[Depends(verify_user_access)])
def delete_book(book_id:int,db=Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise BookNotFoundException()
    db.delete(book)
    db.commit()
    return{
        "message":"Book successfully deleted"
    }
    

@router.post("/books/{book_id}/purchase",response_model=UserPurchaseResponse)
def purchase_book(book_id:int,db = Depends(get_db),current_user = Depends(get_current_user)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise BookNotFoundException()

    query = (
        update(Book)
        .where(Book.id == book_id,Book.stock_quantity>0)
        .values(stock_quantity=Book.stock_quantity - 1)
    )

    result = db.execute(query)

    if result.rowcount == 0:
        db.rollback()
        raise HTTPException(status_code=400, detail="Book is out of stock")

    new_purchase = Purchase(
        user_id=current_user.id,
        book_id=book_id,
        price_at_purchase=book.price
    )
    db.add(new_purchase)
    db.commit()
    db.refresh(new_purchase)
    return new_purchase

@router.get("/me/purchases",response_model=list[UserPurchaseResponse])
def get_user_purchases(current_user = Depends(get_current_user), db = Depends(get_db)):
    return current_user.purchases

@router.post("/books/{book_id}/reviews")
def create_review(book_id:int,review1:ReviewCreate, db = Depends(get_db),current_user = Depends(review_permitted)):
    existing_review = db.query(Review).filter(current_user.id ==Review.user_id,book_id == Review.book_id).first()
    if existing_review is not None:
        raise HTTPException(
            status_code=400,
            detail="You have already reviewed this book"
        )
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise BookNotFoundException()

    new_review = Review(
        user_id = current_user.id,
        book_id = book.id,
        rating = review1.rating,
        text = review1.text
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

@router.get("/books/{book_id}/reviews",response_model=list[ReviewResponse])
def get_reviews(book_id:int,db = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise BookNotFoundException()
    return book.reviews

@router.delete("/reviews/{review_id}")
def delete_review(review_id:int,current_user = Depends(get_current_user),db = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if review is None:
        raise ReviewNotFoundException()
    if (current_user.role == "admin") or (review.user_id == current_user.id):
        db.delete(review)
        db.commit()

        return{
            "message":"review deleted"
        }
    else:
        raise HTTPException(status_code=403, detail="You don't have permission to delete this review")

