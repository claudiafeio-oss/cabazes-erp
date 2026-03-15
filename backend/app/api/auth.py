from jose import jwt, JWTError
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.security import create_access_token, verify_password
from app.models.user import User
from app.schemas.auth import LoginRequest, Token


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> Token:
    user = db.execute(select(User).where(User.email == payload.email)).scalar_one_or_none()
    if user is None or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials")
    token = create_access_token(str(user.id))
    return Token(access_token=token)


@router.post("/refresh", response_model=Token)
def refresh(payload: dict, db: Session = Depends(get_db)) -> Token:
    token = payload.get("token")
    if not token:
        raise HTTPException(status_code=400, detail="token required")
    try:
        decoded = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        subject = decoded.get("sub")
    except JWTError as exc:
        raise HTTPException(status_code=401, detail="invalid token") from exc
    if subject is None:
        raise HTTPException(status_code=401, detail="invalid token")
    user = db.get(User, int(subject))
    if user is None:
        raise HTTPException(status_code=401, detail="invalid token")
    new_token = create_access_token(str(user.id))
    return Token(access_token=new_token)
