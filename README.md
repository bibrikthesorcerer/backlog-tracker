<div align="center">

# 🎬 Backlog

### Personal media consumption tracker

Track movies, books, games, and other media through a clean lifecycle system.

![Python](https://img.shields.io/badge/python-3.x-blue?style=for-the-badge&logo=python)
![Django](https://img.shields.io/badge/django-backend-092E20?style=for-the-badge&logo=django)
![PostgreSQL](https://img.shields.io/badge/postgresql-database-316192?style=for-the-badge&logo=postgresql)
![Celery](https://img.shields.io/badge/celery-task_queue-37814A?style=for-the-badge&logo=celery)
![Redis](https://img.shields.io/badge/redis-broker-DC382D?style=for-the-badge&logo=redis)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)

</div>

---

## Overview

Most people have a growing list of media they want to consume someday:

- Movies 🎥
- Books 📚
- Games 🎮
- TV shows 📺
- Anything else worth experiencing

**Backlog** helps users organize that chaos.

Users can move content through a simple lifecycle:

```text
Wishlist → In Progress → Completed / Dropped
```

The platform also periodically sends curation emails to encourage users to finally consume the media sitting in their backlog or to continue consuming media which is already in progress.

---

# Features

- 📦 Media backlog management
- 🔄 FSM-powered lifecycle transitions
- 🔐 User authentication via Django sessions & cookies
- ⚡ REST API
- 📨 Periodic recommendation emails using Celery
- 🗄 PostgreSQL persistence
- 🛠 Infrastructure automation with Ansible
- 🧪 Local development powered by Poetry

---

# 🏗 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python + Django |
| Database | PostgreSQL |
| Async Tasks | Celery |
| Message Broker | Redis |
| Dependency Management | Poetry |
| Infrastructure | Ansible |

---

# ⚙️ Installation

## Clone Repository

```bash
git clone <repository-url>
cd backlog
```

---

# 💻 Local Development

## Requirements

- [Python](https://www.python.org/)
- [Poetry](https://python-poetry.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Redis](https://redis.io/)

---

## Install Dependencies

```bash
poetry install
```

---

## Configure Environment

Backlog uses [Dynaconf](https://dynaconf.com) with `.secrets.toml`.

An example configuration file is included:

```bash
example.secrets.toml
```

Create your local configuration:

```bash
cp example.secrets.toml .secrets.toml
```

Update the values as needed.

---

## Run Development Server

```bash
$(poetry env activate)
python manage.py runserver
```

---

# 🧰 Ansible Setup

You can bootstrap the project locally using Ansible

First off, create `inventory.ini` with host nodes.  
Then create a `vault/postgres_password.yml` if you intend to use PostgreSQL locally on host node.  
It should contain `postgres_admin_password` and `postgres_password`, which will be used to manage `postgres` user and project-specific DB user.
```yml
postgres_admin_password: PASS
postgres_password: PASS
```
Finally, encrypt it using ansible vault:

```bash
ansible-vault encrypt deploy/vault/postgres_password.yml
```

Then you can run 

```bash
ansible-playbook -i deploy/inventory.ini deploy/site.yml --ask-vault-pass
```
*Or store vault password in a file and point it to Ansible:*
```bash
ansible-playbook -i deploy/inventory.ini deploy/site.yml --vault-password-file .vault_pass
```

---

# 📡 API Documentation

Swagger UI is available at:

```text
/api/schema/swagger-ui
```

---

# 📘 Usage

Backlog currently uses Django session authentication with cookies + CSRF protection.

Typical API flow:

1. Register a user
2. Login to obtain:
   - Session cookie
   - CSRF token
3. Make authenticated requests

---

## 1️⃣ Register

```bash
curl -X POST http://localhost:8000/api/auth/register \
  --json '{
    "username": "demo",
    "password": "password123"
  }'
```

---

## 2️⃣ Login

```bash
curl -X POST http://localhost:8000/api/auth/login \
  --json '{
    "username": "demo",
    "password": "password123"
  }' \
  -c cookies.txt -i
```

After login:

- Session cookies are stored in `cookies.txt`
- The response headers contain the CSRF token

---

## 3️⃣ Create Media Item

Make requests. CSRF token must be passed manually to `X-CSRFToken` HTTP header:
```bash
curl -X POST http://localhost:8000/media_items/ \
  --json '{
    "title": "Disco Elysium",
    "media_type": "game"
  }' \
  -H "X-CSRFToken: <csrf-token>" \
  -b cookies.txt
```

---

## 🔐 Authentication Summary

Backlog uses:

- Django session authentication
- Cookie-based sessions
- CSRF protection for state-changing requests

Authenticated requests require:

- Valid session cookie
- `X-CSRFToken` header

---

# 🔄 Media Lifecycle

Backlog uses finite-state transitions to track content progress:

```text
Wishlist
   ↓
In Progress
   ├──→ Completed
   └──→ Dropped
```

---

# 📨 Recommendation System

Periodic Celery tasks send users daily email curations based on their backlog.

The goal is simple:

> Help users actually consume the media they keep saving for later.

---

# Roadmap

- [ ] User statistics
- [ ] External metadata integrations
- [ ] Dedicated frontend application

---

# 📄 License

Licensed under the MIT License.

---