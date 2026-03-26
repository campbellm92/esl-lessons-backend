from datetime import timedelta
from fastapi import APIRouter, Security, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_active_user
from app.core.config import settings
from app.core.security import create_access_token
from app.schemas.user import UserCreate, User, Token
from app.services.auth_service import AuthService

router = APIRouter()

@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Security(get_db)):
    if AuthService.is_email_taken(db, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered."
        )
    
    return AuthService.create_user(db=db, user=user)

@router.post("/login", response_model=Token)
def login_user(form_data: OAuth2PasswordRequestForm = Security(), db: Session = Security(get_db)):
    ''' 
    Note: form_data.username is used here because the fastAPI OAuth flow specifies that you must send
    username and password as form data (email or anything else won't work)
    In any case, email does work as username. Just something to be aware of when testing.
    '''
    user = AuthService.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=User)
def read_users_me(current_user: User = Security(get_current_active_user)):
    return current_user

