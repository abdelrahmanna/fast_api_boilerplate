# 🚀 FastAPI Boilerplate

A modern, production-ready FastAPI backend starter kit with:

- JWT authentication (access & refresh tokens)
- Secure password hashing (bcrypt)
- Redis-based token/code management (refresh, reset, verification)
- Email/phone verification flows
- Password reset endpoints
- Automated testing (pytest, httpx)
- Alembic migrations (SQLAlchemy)
- Command-line code generation for models, CRUD, and tests
- Clean, extensible code structure

---

## Features

- **JWT Auth**: Secure login/registration with access and refresh tokens, stored/validated in Redis.
- **Password Reset**: Request and confirm reset via email token (no password leak).
- **Email/Phone Verification**: Verification codes and tokens managed in Redis.
- **Role-Ready Models**: Modular user model; easy to extend for teams, roles, etc.
- **Async-Ready**: Fully compatible with async endpoints and background tasks.
- **Test Suite**: Full pytest + httpx setup for
