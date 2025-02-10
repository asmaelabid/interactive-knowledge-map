# Interactive Knowledge Map

A web application for visualizing and managing course dependencies using an interactive graph interface. Built with Vue.js, FastAPI, and PostgreSQL.

## 🚀 Features

- Interactive D3.js graph visualization
- Course dependency management
- Dark/Light theme support
- Real-time graph updates

## 🛠️ Tech Stack

**Frontend:**
- Vue 3
- TypeScript
- Tailwind CSS
- D3.js
- Pinia (State Management)

**Backend:**
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic (Database Migrations)

## 📋 Prerequisites

- Docker and Docker Compose
- PostgreSQL database (or a cloud database service like Neon)

## 🔧 Setup & Installation

1. **Clone the repository**

  ```bash
  git clone https://github.com/yourusername/interactive-knowledge-map.git
  ```

  ```
  cd interactive-knowledge-map
  ```

2. **Environment Configuration**
  - Create the following .env files:
    - Frontend directory .env:

      ```
      VITE_BACKEND_URL=http://localhost:8000/api/v1
      ```

    - Backend directory .env:

      ```
      DATABASE_URL=postgresql+asyncpg://user:password@host:port/database_name
      ```

  > ⚠️ Make sure to replace the database credentials with your own in the .env file

3. **Build and Run with Docker**

   ```
   docker-compose up --build
   ```

## The application will be available at:
  - Frontend: http://localhost:80
  - Backend API: http://localhost:8000


## 🔄 API Endpoints
- ```GET /api/v1/courses/``` - List all courses
- ```POST /api/v1/courses/``` - Create a new course
- ```GET /api/v1/courses/{course_id}``` - Get course details
- ```PUT /api/v1/courses/{course_id}``` - Update a course
- ```DELETE /api/v1/courses/{course_id}``` - Delete a course

