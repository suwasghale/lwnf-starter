# LWNF Backend

A production-grade Django backend built for the **Little World Nepal Foundation (LWNF)**.

This project is designed with a strong focus on maintainability, scalability, security, and clean architecture. It serves as the backend powering the LWNF platform, providing RESTful APIs, background task processing, media management, and administrative tools.

> **Project Status:** 🚧 Active Development

---

## Goals

* Build a production-ready backend using modern Django practices.
* Follow a feature-based architecture with reusable components.
* Provide a secure and scalable REST API.
* Support asynchronous task processing.
* Be fully containerized with Docker.
* Be deployable on a Linux VPS.
* Maintain a clean and extensible codebase suitable for long-term growth.

---

## Planned Technology Stack

| Category           | Technology              |
| ------------------ | ----------------------- |
| Language           | Python 3.13+            |
| Framework          | Django 5.x              |
| API                | Django REST Framework   |
| Database           | PostgreSQL              |
| Cache              | Redis                   |
| Background Tasks   | Celery + Celery Beat    |
| API Documentation  | drf-spectacular         |
| Storage            | Cloudflare R2           |
| Authentication     | JWT                     |
| Containerization   | Docker & Docker Compose |
| Web Server         | Gunicorn + Nginx        |
| Package Management | uv                      |
| Testing            | Pytest                  |

---

## Project Structure

```text
backend/
├── apps/
├── config/
├── core/
├── infrastructure/
├── docker/
├── docs/
├── locale/
├── logs/
├── media/
├── scripts/
├── static/
├── tests/
├── manage.py
├── pyproject.toml
└── README.md
```

---

## Current Progress

* ✅ Project initialization
* ✅ Modular settings architecture
* ✅ Environment configuration
* 🚧 Infrastructure setup (Docker, PostgreSQL, Redis)
* ⏳ Authentication system
* ⏳ API development
* ⏳ Production deployment

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
