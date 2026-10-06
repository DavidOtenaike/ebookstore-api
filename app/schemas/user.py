from pydantic import BaseModel,ConfigDict,EmailStr,Field
from decimal import Decimal
import datetime

class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    id:int
    email:EmailStr
    role:str 
    created_at: datetime.datetime
    model_config = ConfigDict(from_attributes=True)

class Login(BaseModel):
    email:str
    password:str

class BookCreate(BaseModel):
    title:str
    description:str
    price: Decimal
    stock_quantity: int
    author_id : int
    category_ids : list[int] | None = None

class BookUpdate(BaseModel):
    title:str | None = None
    description:str | None = None
    price: Decimal | None = None
    stock_quantity: int | None = None
    author_id : int | None = None
    category_ids : list[int] | None = None

class SimpleAuthorResponse(BaseModel):
     id : int
     name :str
     model_config = ConfigDict(from_attributes=True)

class SimpleCategoryResponse(BaseModel):
     id : int
     name :str
     model_config = ConfigDict(from_attributes=True)

class BookResponse(BaseModel):
        id : int
        title:str
        description:str
        price: Decimal
        stock_quantity: int
        author : SimpleAuthorResponse
        categories : list[SimpleCategoryResponse]
        model_config = ConfigDict(from_attributes=True)     

class PaginatedBooksResponse(BaseModel):
    items: list[BookResponse]
    total: int
    page: int
    limit: int
    pages: int  
    model_config = ConfigDict(from_attributes=True)     

class SimpleBookResponse(BaseModel):
    id:int
    title:str
    price:Decimal
    model_config = ConfigDict(from_attributes=True)     
     
class UserPurchaseResponse(BaseModel):
     id : int
     user_id : int
     book : SimpleBookResponse
     purchased_at : datetime.datetime
     price_at_purchase : Decimal
     model_config = ConfigDict(from_attributes=True)

class ReviewCreate(BaseModel):
    rating : int = Field(le=5,ge=1)
    text : str

class ReviewResponse(BaseModel):
     id : int
     user_id : int
     book_id : int
     rating : int
     text : str
     created_at : datetime.datetime
     model_config = ConfigDict(from_attributes=True)
          
     



