from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, EmailStr, Field


class UserRole(str, Enum):
    admin = "admin"
    operator = "operator"
    viewer = "viewer"


class NodeStatus(str, Enum):
    online = "online"
    degraded = "degraded"
    offline = "offline"


class SessionStatus(str, Enum):
    active = "active"
    ended = "ended"
    revoked = "revoked"


class User(BaseModel):
    id: str
    email: EmailStr
    role: UserRole
    password_hash: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Node(BaseModel):
    id: str
    name: str
    region: str
    status: NodeStatus = NodeStatus.online
    endpoint: str
    capacity: int = 1000
    load: int = 0


class Session(BaseModel):
    id: str
    user_id: str
    node_id: str
    status: SessionStatus = SessionStatus.active
    bytes_up: int = 0
    bytes_down: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

