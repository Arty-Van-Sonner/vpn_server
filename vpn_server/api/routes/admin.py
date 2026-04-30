from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status

from vpn_server.db import nodes, sessions, users
from vpn_server.deps import require_role
from vpn_server.models import Node, Session, UserRole
from vpn_server.schemas import NodeCreate, NodeRead, SessionRead, UserRead

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", response_model=list[UserRead])
def list_users(_: UserRead = Depends(require_role(UserRole.admin, UserRole.operator))) -> list[UserRead]:
    return [UserRead(id=u.id, email=u.email, role=u.role, is_active=u.is_active) for u in users.values()]


@router.post("/nodes", response_model=NodeRead, status_code=status.HTTP_201_CREATED)
def create_node(
    payload: NodeCreate, _: UserRead = Depends(require_role(UserRole.admin))
) -> NodeRead:
    node = Node(
        id=str(uuid4()),
        name=payload.name,
        region=payload.region,
        endpoint=payload.endpoint,
        capacity=payload.capacity,
    )
    nodes[node.id] = node
    return NodeRead(**node.model_dump())


@router.get("/nodes", response_model=list[NodeRead])
def list_nodes(_: UserRead = Depends(require_role(UserRole.admin, UserRole.operator, UserRole.viewer))) -> list[NodeRead]:
    return [NodeRead(**node.model_dump()) for node in nodes.values()]


@router.post("/sessions/{user_id}/{node_id}", response_model=SessionRead, status_code=status.HTTP_201_CREATED)
def create_session(
    user_id: str, node_id: str, _: UserRead = Depends(require_role(UserRole.admin, UserRole.operator))
) -> SessionRead:
    if user_id not in users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if node_id not in nodes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Node not found")

    session = Session(id=str(uuid4()), user_id=user_id, node_id=node_id)
    sessions[session.id] = session
    return SessionRead(**session.model_dump())


@router.get("/sessions", response_model=list[SessionRead])
def list_sessions(_: UserRead = Depends(require_role(UserRole.admin, UserRole.operator, UserRole.viewer))) -> list[SessionRead]:
    return [SessionRead(**session.model_dump()) for session in sessions.values()]

