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

poetry install
docker compose build
docker compose up -d
poetry run alembic upgrade head


## Project Structure

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

## Team


| Developer            | Responsibility |
|---------------------------------------|
| Kateryna Hryhorieva  | 
| Kostiantyn Yesypenko | 