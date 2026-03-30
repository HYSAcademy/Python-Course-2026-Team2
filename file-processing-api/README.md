# File Processing API

Backend service for processing and storing files.

---

## Tech Stack

- FastAPI — API framework  
- PostgreSQL — database  
- SQLModel — ORM  
- Alembic — database migrations  
- Poetry — dependency management  
- Docker + Docker Compose — containerization  

---

## Setup Instructions

Run the following commands to start the project:
```
poetry install
docker compose build
docker compose up -d
poetry run alembic upgrade head

in db run CREATE EXTENSION IF NOT EXISTS vector;
```

## Project Structure
```
file-processing-api/
│
├── migrations/
│   └── versions/
│
├── src/
│   └── file_processing_api/
│       ├── api/
│       ├── db/
│       ├── models/
│       └── main.py
│   
├── tests/
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── poetry.lock
├── pyproject.toml
└── README.md
```
## Team


## 👥 Team

| Developer | Area | Responsibilities |
|-----------|------|------------------|
| **Kateryna Hryhorieva** | Part 1 | Poetry project • FastAPI setup • Project structure • PostgreSQL configuration • Docker setup • Global exception middleware |
| **Kostiantyn Yesypenko** | Part 2 | Upload endpoint • File validation • Archive extraction • Async processing • Database storage • API response |