from pydantic import BaseModel, EmailStr

from vpn_server.models import NodeStatus, SessionStatus, UserRole


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: UserRole = UserRole.viewer


class UserRead(BaseModel):
    id: str
    email: EmailStr
    role: UserRole
    is_active: bool


class NodeCreate(BaseModel):
    name: str
    region: str
    endpoint: str
    capacity: int = 1000


class NodeRead(BaseModel):
    id: str
    name: str
    region: str
    endpoint: str
    status: NodeStatus
    capacity: int
    load: int


class SessionRead(BaseModel):
    id: str
    user_id: str
    node_id: str
    status: SessionStatus
    bytes_up: int
    bytes_down: int

