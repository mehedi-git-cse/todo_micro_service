# FastAPI Todo Application

A simple TODO API built with FastAPI following best practices and clean architecture.

## Project Structure

```
fastapi_app/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Entry point
│   ├── core/                   # Settings, config
│   │   └── config.py
│   ├── models/                 # All Pydantic models
│   │   └── todo_model.py
│   ├── controllers/            # Business logic
│   │   └── todo_controller.py
│   ├── routes/                 # API endpoints
│   │   └── todo_route.py
│   └── services/              # External integrations (if needed)
├── requirements.txt
└── README.md
```

## Features

- CRUD operations for Todo items
- Input validation using Pydantic models
- Clean architecture with separation of concerns
- Configuration management
- Error handling
- API documentation with Swagger UI

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

To run the application:

```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

API documentation will be available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

- `GET /`: Welcome message
- `GET /api/v1/todos/`: List all todos
- `POST /api/v1/todos/`: Create a new todo
- `GET /api/v1/todos/{todo_id}`: Get a specific todo
- `PUT /api/v1/todos/{todo_id}`: Update a todo
- `DELETE /api/v1/todos/{todo_id}`: Delete a todo
