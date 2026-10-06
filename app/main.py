from fastapi import FastAPI,Request
from app.auth.routers import router
from fastapi.responses import JSONResponse
from app.core.exceptions import UserNotFoundException,UnauthorizedException,InvalidCredentialsException,PurchaseRequiredException,UserAlreadyExistsException,InvalidDetailsException,InvalidRoleException,BookNotFoundException,BookAlreadyExistsException,ReviewNotFoundException

app = FastAPI()
app.include_router(router)

@app.exception_handler(UserNotFoundException)
async def user_not_found_handler(request:Request,exc:UserNotFoundException):
    return JSONResponse(
        status_code=404,
        content ={
            "error":"USER_NOT_FOUND",
            "message": "User does not exist"
        })

@app.exception_handler(InvalidCredentialsException)
async def invalid_credentials_handler(request:Request,exc:InvalidCredentialsException):
    return JSONResponse(
        status_code=401,
        content ={
            "error":"INVALID_CREDENTIALS",
            "message": "Credentials are invalid"
        })

@app.exception_handler(UnauthorizedException)
async def user_unauthorized_handler(request:Request,exc:UnauthorizedException):
    return JSONResponse(
        status_code=403,
        content ={
            "error":"UNAUTHORIZED",
            "message": "User logged in but not permitted"
        })

@app.exception_handler(PurchaseRequiredException)
async def purchase_required_handler(request:Request,exc:PurchaseRequiredException):
    return JSONResponse(
        status_code=403,
        content ={
            "error":"UNAUTHORIZED",
            "message": "User must purchase a book before review"
        })

@app.exception_handler(Exception)
async def generic_exception_handler(request : Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content= {
            "error":"INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occured"
        }
    )

@app.exception_handler(UserAlreadyExistsException)
async def user_already_exists_exception_handler(request:Request,exc:UserAlreadyExistsException):
    return JSONResponse(
            status_code=409,
            content ={
                "error":"ALREADY_EXISTS",
                "message": "User already exists"
            })

@app.exception_handler(InvalidDetailsException)
async def invalid_details_handler(request:Request,exc:InvalidDetailsException):
    return JSONResponse(
        status_code=401,
        content ={
            "error":"INVALID_DETAILS",
            "message": "Details are invalid"
        })

@app.exception_handler(InvalidRoleException)
async def invalid_role_handler(request:Request,exc:InvalidRoleException):
    return JSONResponse(
        status_code=400,
        content ={
            "error":"INVALID_ROLE",
            "message": "Role is invalid"
        })

@app.exception_handler(BookNotFoundException)
async def book_not_found_handler(request:Request,exc:BookNotFoundException):
    return JSONResponse(
        status_code=404,
        content ={
            "error":"BOOK_NOT_FOUND",
            "message": "Book does not exist"
        })

@app.exception_handler(BookAlreadyExistsException)
async def book_already_exists_exception_handler(request:Request,exc:UserAlreadyExistsException):
    return JSONResponse(
            status_code=409,
            content ={
                "error":"ALREADY_EXISTS",
                "message": "Book already exists"
            })

@app.exception_handler(ReviewNotFoundException)
async def review_not_found_handler(request:Request,exc:ReviewNotFoundException):
    return JSONResponse(
        status_code=404,
        content ={
            "error":"REVIEW_NOT_FOUND",
            "message": "Review does not exist"
        })