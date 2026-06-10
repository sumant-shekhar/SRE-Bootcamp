# SRE Bootcamp: Student Management API

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A robust, self-paced SRE roadmap project designed to bridge the gap between local development and production-grade reliability. This project provides a standard Flask REST API for managing student records, serving as a foundation for implementing SRE practices like CI/CD, monitoring, containerization, and orchestration.

## Description

This project is a Student Management System built with Python and Flask. It provides a full set of CRUD (Create, Read, Update, Delete) operations via a RESTful API. 

**Key Features:**
- **RESTful API:** Clean and versioned endpoints (`/v1/api/...`).
- **Database Integration:** Uses SQLAlchemy with SQLite (default) and support for PostgreSQL/MySQL via environment variables.
- **Migrations:** Managed database schema changes using Flask-Migrate (Alembic).
- **Testing:** Comprehensive unit and integration tests using Pytest.
- **Operational Ready:** Includes health check endpoints and logging.

## Installation

This project uses a `Makefile` to simplify setup.

### Prerequisites
- Python 3.8+
- `pip` and `venv`

### Setup Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sumant-shekhar/SRE-Bootcamp.git
   cd SRE-Bootcamp
   ```

2. **Install dependencies:**
   This will create a virtual environment and install all required packages.
   ```bash
   make install
   ```

3. **Initialize the database:**
   ```bash
   make init-db   # Only for the first time
   make migrate   # Generate migration scripts
   make upgrade   # Apply migrations to database
   ```

## Usage

### Running the Application

To start the development server:
```bash
make run
```
The API will be available at `http://127.0.0.1:4000`.

### API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/v1/api/students/` | List all students |
| `GET` | `/v1/api/students/<id>` | Get details of a specific student |
| `POST` | `/v1/api/students/` | Create a new student |
| `PUT` | `/v1/api/students/<id>` | Update an existing student |
| `DELETE` | `/v1/api/students/<id>` | Remove a student record |
| `GET` | `/v1/api/healthcheck/` | Service health status |

### Example Requests

**Create a Student:**
```bash
curl -X POST http://127.0.0.1:4000/v1/api/students/ \
     -H "Content-Type: application/json" \
     -d '{"name": "John Doe", "email": "john.doe@example.com", "age": 21}'
```

**Get All Students:**
```bash
curl http://127.0.0.1:4000/v1/api/students/
```

### Running Tests
```bash
pytest
```

## Support

For support, please open an issue in the GitHub repository or contact the maintainers directly.

## Roadmap

This project is designed to evolve into a full SRE showcase. Future steps include:
- [ ] **Dockerization:** Create Dockerfiles and docker-compose for easy orchestration.
- [ ] **CI/CD Pipeline:** Implement GitHub Actions for automated testing and deployment.
- [ ] **Monitoring:** Integrate Prometheus and Grafana for metrics visualization.
- [ ] **Logging:** Centralized logging with ELK or Loki.
- [ ] **Infrastructure as Code:** Deploy using Terraform or Pulumi.

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the Project.
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the Branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

## Authors and Acknowledgment

- **Sumant Shekhar** - *Initial work* - [Sumant-Shekhar](https://github.com/Sumant-Shekhar)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Project Status

This project is currently in active development as part of the SRE Bootcamp series.
