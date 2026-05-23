from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from typing import Annotated
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from datetime import timedelta,datetime,timezone
import jwt,os
import dotenv

from sqlalchemy.orm import Session
from core import session_int
from schemas import RegisterRequest,TokenResponse, UserResponse
from tables import User
import uuid


dotenv.load_dotenv(override=True)

password_hash=PasswordHash([Argon2Hasher()])
oauth_scheme=OAuth2PasswordBearer(tokenUrl='/v1/auth/login')

ALGORITHM=os.getenv("JWT_ALGORITHM")
SECRET_KEY=os.getenv("SECRET_KEY")


router=APIRouter(prefix="/v1/auth",tags=["jwt_auth"])


def pass_hash(password: str):
    return password_hash.hash(password)


def pass_verify(password:str,input_hash: str):
    verify_status=password_hash.verify(password,input_hash)
    return verify_status



def create_access_token(data: dict,valid_time: timedelta = timedelta(minutes=15)):
    exp_time=datetime.now(timezone.utc)+valid_time

    #to_encode=data.copy()
    data.update({"exp":exp_time,"iat":datetime.now(timezone.utc)})
    token=jwt.encode(payload=data,algorithm=ALGORITHM,key=SECRET_KEY)
    return token

def authenticate_user(username: str, password: str, db: Session):
    error_response=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"message":"Incorrect username or password"},
        headers={"WWW-Authenticate": "Bearer"}
    )
    existing_user_data= db.query(User).filter(User.username == username).first()
    if not existing_user_data:
        raise error_response

    if not pass_verify(password,existing_user_data.password_hash):
        raise error_response

    return existing_user_data


def get_current_user(db: session_int, token:Annotated[str,Depends(oauth_scheme)]):
    error_response=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid access token",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload=jwt.decode(jwt=token,key=SECRET_KEY,algorithms=[ALGORITHM])
        user_id=payload.get("sub")
        if not user_id:
            raise error_response
        
    except jwt.exceptions.InvalidTokenError:
        raise error_response
    
    user_data=db.query(User).filter(User.id==uuid.UUID(user_id)).first()
    if not user_data:
        raise error_response
    
    return UserResponse.model_validate(user_data)


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def sign_up(user_auth_info: RegisterRequest, db: session_int):
    existing_username = db.query(User).filter(User.username == user_auth_info.username).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )

    existing_email = db.query(User).filter(User.email == user_auth_info.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists",
        )

    user = User(
        email=user_auth_info.email,
        username=user_auth_info.username,
        password_hash=pass_hash(user_auth_info.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message":"Sign Up Successful"}
    )


@router.post("/login")
def login_for_access_token(user_auth_info: Annotated[OAuth2PasswordRequestForm,Depends()], db: session_int):
    valid_user=authenticate_user(user_auth_info.username,user_auth_info.password,db=db)
    
    if valid_user:
        access_token=create_access_token(
            data={"sub":str(valid_user.id),"user":valid_user.username},
            valid_time=timedelta(minutes=20)
        )
    

    return TokenResponse(access_token=access_token,token_type="bearer")

    
@router.get("/getuser")
def read_user(current_user: Annotated[UserResponse,Depends(get_current_user)]):
    return current_user




