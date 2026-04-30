# VPN Server

Control plane on FastAPI, tunnel node on Rust, and admin frontend on React.

## Project layout

- `vpn_server/` - FastAPI backend (auth, RBAC, admin API).
- `src/` - Rust UDP tunnel node skeleton.
- `admin/` - React + TypeScript admin panel.

## Backend quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn vpn_server.api.main:app --reload
```

Default seeded admin:

- email: `admin@vpn.local`
- password: `admin123`

API base URL: `http://localhost:8000/api/v1`

## Admin panel quickstart

```bash
cd admin
npm install
npm run dev
```

Panel URL: `http://localhost:5173`

## Tunnel node quickstart

```bash
cargo run -- --bind 0.0.0.0:51820
```

Current Rust implementation is a secure-ready skeleton for packet loop and logging.
Next step is integrating TUN I/O and authenticated session keys from control plane.