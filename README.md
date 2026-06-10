# SRE-Bootcamp
A self-paced, problem-first SRE roadmap designed to bridge the gap between local development and production-grade reliability.

# 1. Flask REST API
A basic, standard REST API built with Python and Flask. 
This includes database support and cross-origin resource sharing (CORS).

## Project Structure
* `requirements.txt` - List of project dependencies.
* `README.md` - Project documentation.
* `app.py` - CRUD source code

## Tech Stack
* Framework: [Flask](https://palletsprojects.com)
* ORM / Database: [Flask-SQLAlchemy](https://palletsprojects.com)
* frontend:[Flask-CORS](https://corydolphin.com)


## Setup

### 1. Clone
```bash
git clone <https://github.com/sumant-shekhar/SRE-Bootcamp.git>
cd <SRE-Bootcamp>
```

### 2. Install
```bash
make install
```

### 3. Set environment variable

Mac/Linux:
```bash
export DATABASE_URL=sqlite:///database.db
```

### 4. Run
```bash
make run
```

App runs at:
```
http://127.0.0.1:4000
```

---

## API

Base path:
```
/v1/api/students
```

Endpoints:

- GET `/v1/api/students/`
- GET `/v1/api/students/<id>`
- POST `/v1/api/students/`
- PUT `/v1/api/students/<id>`
- DELETE `/v1/api/students/<id>`
- healthcheck `/v1/api/healthcheck/`

---

## Healthcheck

```
GET /healthcheck
```

---