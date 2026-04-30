from uuid import uuid4

from fastapi import APIRouter, HTTPException, status

from vpn_server.core.security import create_access_token, hash_password, verify_password
from vpn_server.db import users
from vpn_server.models import User
from vpn_server.schemas import LoginRequest, TokenResponse, UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate) -> UserRead:
    if any(u.email == payload.email for u in users.values()):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")

    user = User(
        id=str(uuid4()),
        email=payload.email,
        role=payload.role,
        password_hash=hash_password(payload.password),
    )
    users[user.id] = user
    return UserRead(id=user.id, email=user.email, role=user.role, is_active=user.is_active)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest) -> TokenResponse:
    user = next((u for u in users.values() if u.email == payload.email), None)
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return TokenResponse(access_token=create_access_token(user.id, user.role.value))

