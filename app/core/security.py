from jose import jwt,JWTError
from passlib.context import CryptContext
from datetime import datetime,timedelta,timezone
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from fastapi import HTTPException,Depends
from app.database.database import get_db
from app.core.exceptions import UserNotFoundException,UnauthorizedException,InvalidCredentialsException,PurchaseRequiredException
from app.models.user import User,Purchase


oauth2scheme = OAuth2PasswordBearer(tokenUrl="login")

pwd_context = CryptContext(schemes=["bcrypt"],deprecated = "auto")
def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

def create_access_token(data):
    payload = data.copy()
    expire = datetime.now(timezone.utc)+timedelta(minutes=30)
    payload.update({"exp":expire})
    token = jwt.encode(payload,settings.SECRET_KEY,algorithm=settings.ALGORITHM)
    return token

def get_current_user(token:str = Depends(oauth2scheme), db = Depends(get_db)):
    try:
        payload = jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
    except JWTError:
        raise InvalidCredentialsException()
    user_id = payload.get("sub")
    if user_id is None:
        raise InvalidCredentialsException()
    current_user = db.query(User).filter(User.id == int(user_id)).first()
    if current_user is None:
        raise UserNotFoundException()
    return current_user

def verify_user_access(current_user = Depends(get_current_user)):
    if current_user.role != "admin":
        raise UnauthorizedException()
    return current_user

def review_permitted(book_id:int, current_user = Depends(get_current_user),db=Depends(get_db)):
    permitted_user = db.query(Purchase).filter(current_user.id==Purchase.user_id, Purchase.book_id==book_id).first()
    if permitted_user is None:
        raise PurchaseRequiredException()
    return current_user

