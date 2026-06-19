# SRE Bootcamp: Student Management API

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This project provides a standard Flask REST API for managing student records, serving as a foundation for implementing SRE practices such as CI/CD, monitoring, containerization, and orchestration.

---

## Description

This project is a Student Management System built with Python and Flask. It provides a complete set of CRUD (Create, Read, Update, Delete) operations through a RESTful API.

### Key Features

* RESTful API with versioned endpoints (`/v1/api/...`)
* Student record management with CRUD operations
* SQLAlchemy ORM integration
* Database migrations using Flask-Migrate (Alembic)
* SQLite support by default
* Environment-based database configuration
* Health check endpoint for operational readiness
* Multi-stage Docker build for optimized image size
* Runtime environment variable injection
* Semantic Versioning (SemVer) for Docker image tagging

---

## Installation

### Prerequisites

* Python 3.8+
* pip
* venv

### Clone the Repository

```bash
git clone https://github.com/sumant-shekhar/SRE-Bootcamp.git
cd SRE-Bootcamp
```

### Install Dependencies

```bash
make install
```

### Initialize Database

Run these commands the first time only:

```bash
make init-db
make migrate
make upgrade
```

---

## Usage

### Run the Application

```bash
make run
```

The API will be available at:

```text
http://127.0.0.1:4000
```

---

## Docker Usage

### Build Docker Image

Build using semantic version tags:

```bash
make docker-build VERSION=1.0.0
```

Or manually:

```bash
docker build -t rest-api-service:1.0.0 .
```

### Run Docker Container

Using Makefile:

```bash
make docker-run
```

Or manually:

```bash
docker run \
  --env-file .env \
  -p 4000:4000 \
  rest-api-service:1.0.0
```

### Inject Environment Variables

Using an environment file:

```bash
docker run \
  --env-file .env \
  -p 4000:4000 \
  rest-api-service:1.0.0
```

Or individual variables:

```bash
docker run \
  -e DATABASE_URL=sqlite:///database.db \
  -e FLASK_ENV=production \
  -p 4000:4000 \
  rest-api-service:1.0.0
```

### Stop Container

```bash
make docker-stop
```

### Verify Container

```bash
curl http://localhost:4000/v1/api/healthcheck/
```

---

## API Endpoints

| Method | Endpoint                | Description           |
| ------ | ----------------------- | --------------------- |
| GET    | `/v1/api/students/`     | List all students     |
| GET    | `/v1/api/students/<id>` | Get a student by ID   |
| POST   | `/v1/api/students/`     | Create a student      |
| PUT    | `/v1/api/students/<id>` | Update a student      |
| DELETE | `/v1/api/students/<id>` | Delete a student      |
| GET    | `/v1/api/healthcheck/`  | Health check endpoint |

---

## Example Requests

### Create a Student

```bash
curl -X POST http://127.0.0.1:4000/v1/api/students/ \
-H "Content-Type: application/json" \
-d '{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "age": 21
}'
```

### Get All Students

```bash
curl http://127.0.0.1:4000/v1/api/students/
```

---

## Makefile Commands

```bash
make help
```

Available commands include:

```text
make install
make run
make test
make migrate
make upgrade
make init-db
make docker-build
make docker-run
make docker-stop
make clean
```

---

## Environment Variables

Example `.env` file:

```env
FLASK_APP=app.py
FLASK_ENV=production
DATABASE_URL=sqlite:///database.db
```

These values are injected at container runtime and are not baked into the Docker image.

---

## Image Optimization

The Docker image uses:

* Multi-stage builds
* Minimal runtime image
* Dependency caching
* `.dockerignore` exclusions
* SemVer image tagging

These measures reduce image size and improve deployment efficiency.

---

## Support

For support, please open an issue in the GitHub repository.

---

## Roadmap

* [x] Dockerization with multi-stage builds
* [x] Runtime environment variable injection
* [x] Semantic Versioning for Docker images
* [ ] CI/CD pipeline using GitHub Actions
* [ ] Monitoring with Prometheus and Grafana
* [ ] Centralized logging with ELK or Loki
* [ ] Kubernetes deployment
* [ ] Infrastructure as Code with Terraform

---

## Contributing

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature/my-feature
```

3. Commit your changes

```bash
git commit -m "Add feature"
```

4. Push your branch

```bash
git push origin feature/my-feature
```

5. Open a Pull Request

---

## Author

**Sumant Shekhar**

GitHub: https://github.com/Sumant-Shekhar

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Project Status

This project is actively maintained as part of the SRE Bootcamp learning roadmap and continues to evolve with production-focused DevOps and SRE practices.
