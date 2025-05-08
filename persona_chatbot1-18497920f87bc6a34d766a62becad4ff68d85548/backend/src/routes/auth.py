from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas.user import UserCreate, UserLogin, UserOut, TokenRefresh
from ..database import get_db
from ..services import auth
from ..models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = auth.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return auth.create_user(db=db, user=user)

@router.post("/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    result = auth.authenticate_user(db, email=user.email, password=user.password)
    if not result:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    user, access_token, refresh_token = result
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh")
async def refresh_token(token_data: TokenRefresh, db: Session = Depends(get_db)):
    email = auth.verify_refresh_token(token_data.refresh_token)
    if not email:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create new access token
    access_token = auth.create_access_token({"sub": email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
async def get_current_user_info(current_user: User = Depends(auth.get_current_user)):
    """Get the current authenticated user's information."""
    return current_user