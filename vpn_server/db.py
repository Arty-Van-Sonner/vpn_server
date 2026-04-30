from uuid import uuid4

from vpn_server.core.security import hash_password
from vpn_server.models import Node, Session, User, UserRole

users: dict[str, User] = {}
nodes: dict[str, Node] = {}
sessions: dict[str, Session] = {}


def seed_data() -> None:
    if users:
        return

    admin = User(
        id=str(uuid4()),
        email="admin@vpn.local",
        role=UserRole.admin,
        password_hash=hash_password("admin123"),
    )
    users[admin.id] = admin

