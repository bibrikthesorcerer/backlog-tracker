<div align="center">

# 🎬 Backlog

### Personal media consumption tracker

Track movies, books, games, and other media through a clean lifecycle system.

![Python](https://img.shields.io/badge/python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/django-5.2-092E20?style=for-the-badge&logo=django)
![PostgreSQL](https://img.shields.io/badge/postgresql-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/redis-8-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Celery](https://img.shields.io/badge/celery-5.6-37814A?style=for-the-badge&logo=celery&logoColor=white)
![Docker](https://img.shields.io/badge/docker-containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Docker Compose](https://img.shields.io/badge/docker_compose-orchestrated-1D63ED?style=for-the-badge&logo=docker&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)
</div>

---

# Overview

Most people have a growing list of media they want to consume someday:

- Movies 🎥
- Books 📚
- Games 🎮
- TV shows 📺
- Anything else worth experiencing

**Backlog** helps users organize that chaos.

It provides simple tooling to help users track, rate and reflect on different media they want to consume.

Users can move content through a simple lifecycle:

```text
Wishlist → In Progress → Completed / Dropped
```

The platform also periodically sends curation emails to encourage users to finally consume the media sitting in their backlog or to continue consuming media which is already in progress.

---

# Features

- 📦 Track, rate and reflect on movies, books, games and other media in one place
- 🔄 FSM-powered lifecycle management for media content
- 🔐 Session-based authentication with Django
- ⚡ REST API for integration with frontend clients
- 📨 Periodic recommendation emails using Celery
- 🗄 PostgreSQL persistence
- 🐳 Fully containerized development and deployment workflow
- 🧪 Local development powered by Poetry

---

# 🏗 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python + Django + DRF |
| Database | PostgreSQL |
| Async Tasks | Celery |
| Message Broker | Redis |
| Dependency Management | Poetry |
| Containerization | Docker + Docker Compose |

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/bibrikthesorcerer/backlog-tracker.git
cd backlog
```

---


# 🔐 Configuration

Backlog uses [Dynaconf](https://dynaconf.com/) for configuration management.

The project configuration is composed of multiple layers:

- `settings.toml`  
  Stores project-level settings such as logging configuration, pagination, and application defaults.

- `.secrets.toml`  
  Stores sensitive data such as the Django secret key, email credentials, and database credentials.

- `.env` / environment variables  
  Used to override configuration values dynamically. Primarily used in Docker and Docker Compose environments.

- `settings.local.toml` *(optional)*  
  Local machine-specific overrides written in TOML syntax.

Configuration values are loaded in layers, allowing local and environment-specific overrides without modifying the base project configuration. Environment variables take highest priority.

## Environments

Backlog defines three Dynaconf environments:

- `default` — shared base configuration
- `development` — local development settings
- `production` — production-ready overrides

The active environment can be selected using the `BL_MODE` environment variable.

## Initial configuration

Create a local secrets file from the example template:

```bash
cp example.secrets.toml .secrets.toml
```

### Docker Compose Users

> [!IMPORTANT]
> If you are using Docker Compose, the only required variables are:
>
> - `BL_DJANGO__SECRET_KEY`
> - `POSTGRES_PASSWORD`
>
> Create a `.env` file:
>
> ```env
> POSTGRES_PASSWORD=1234
> BL_DJANGO__SECRET_KEY=your_secret_key
> ```
>
>Everything else is configured automatically through container environment variables.

### Local Development Users

For local non-Docker setups, additionally configure:

- PostgreSQL credentials
- Celery's connection settings
- Email credentials

---

# 🐳 Docker Setup (Recommended)

## Requirements

- Docker
- Docker Compose

## Start Services

```bash
docker compose up
```

This starts:

- `web` — Django application
- `postgres` — PostgreSQL database
- `redis` — Celery broker/cache
- `worker` — Celery worker
- `beat` — Celery Beat scheduler

The application then will become available at:

```text
http://localhost:8000
```

---

<details>
<summary><h1>💻 Local Development</h1></summary>

## Requirements

- Python
- Poetry
- PostgreSQL
- Redis

## Install Dependencies

```bash
poetry install
```

## Activate Environment

```bash
$(poetry env activate)
```

## Run Development Server

```bash
python manage.py runserver
```

</details>

<details>
<summary><h1>🧰 Ansible Setup</h1></summary>

You can bootstrap the project locally using Ansible

First off, create `deploy/inventory.ini`, and populate it with host nodes.  

Then create a `deploy/vault/postgres_password.yml` if you intend to use PostgreSQL locally on host node.  
It should contain `postgres_admin_password` and `postgres_password`, which will be used to manage `postgres` user and project-specific DB user.
```yml
postgres_admin_password: PASS
postgres_password: PASS
```
Then encrypt vault using `ansible-vault` command:

```bash
ansible-vault encrypt deploy/vault/postgres_password.yml
```

Then run playbook:

```bash
ansible-playbook -i deploy/inventory.ini deploy/site.yml --ask-vault-pass
```
Or use a vault password file:
```bash
ansible-playbook -i deploy/inventory.ini deploy/site.yml --vault-password-file .vault_pass
```

---
</details>


# 📘 Usage

Backlog currently uses Django session authentication with cookie-based sessions and CSRF protection.

You can interact with the application through:
  - Django REST Framework's Browsable API
  - `curl`
  - any other HTTP client of your choice

Typical workflow:

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

## 3️⃣ Make Authenticated Requests (Create a Media Item)

Authenticated requests require both:
  - session-cookie
  - `X-CSRFToken` header

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
- cookie-based sessions
- CSRF protection for state-changing requests

Authenticated requests require:

- valid session cookie
- valid `X-CSRFToken` header

## 📚 API Documentation

- Swagger UI: `http://localhost:8000/api/schema/swagger-ui/`
- OpenAPI schema: `http://localhost:8000/api/schema/`

---

# 📨 Curation Letters

Periodic Celery tasks send users personalized daily email curations based on their backlog.

These emails highlight:

- media users are highly interested in but haven't started yet
- media they already started but have not finished

The goal is simple:

> Reduce the gap between collecting media and actually experiencing it.

---

# Roadmap

- [ ] User statistics
- [ ] External metadata integrations
- [ ] Dedicated frontend application

---

# 📄 License

Licensed under the MIT License.

---