# Architecture

## Overview

The application is deployed on AWS using a simple containerized architecture.

The current architecture consists of:

- AWS EC2 running Ubuntu
- Nginx as a reverse proxy
- FastAPI application running in Docker
- PostgreSQL running in Docker
- Docker Compose for service management
- HTTPS using Nginx and Let's Encrypt
- CloudWatch for logging and monitoring
- GitHub Actions for CI/CD

The architecture was intentionally kept simple because the assessment prioritizes a working, well-reasoned system over unnecessary complexity.

## Architecture Diagram

![Architecture Diagram](../architecture/architecture-diagram.png)

## High-Level Request Flow

```text
Client
  |
  | HTTPS :443
  v
Nginx
  |
  | Reverse Proxy
  v
FastAPI Application
  |
  | Internal Docker Network
  v
PostgreSQL
```

## Deployment and Monitoring Flow

```text
Developer
    |
    v
GitHub
    |
    v
GitHub Actions
    |
    | Test -> Docker Build -> Deploy
    v
AWS EC2
    |
    +---- Nginx
    +---- FastAPI Container
    +---- PostgreSQL Container
    +---- CloudWatch Agent
```

## Components

### AWS EC2

A small Ubuntu EC2 instance hosts the application.

EC2 was selected because it provides direct control over Linux, Docker, networking, security groups, Nginx, and the deployment process while keeping infrastructure costs low.

### Nginx

Nginx is used as the reverse proxy and public entry point.

It:

- Accepts HTTP/HTTPS requests.
- Handles TLS termination.
- Forwards API requests to FastAPI.
- Keeps the application server behind the reverse proxy.

The FastAPI application runs internally on port `8000`.

### FastAPI

FastAPI provides the REST API and application logic.

It handles:

- API requests
- Request validation
- API-key authentication
- CORS
- Database communication
- Health checks

The health endpoint is:

```text
GET /health
```

Expected response:

```json
{
  "status": "ok",
  "message": "API is running"
}
```

### PostgreSQL

PostgreSQL stores the application's persistent data.

The database communicates with FastAPI through the internal Docker network and is not intended to be publicly accessible.

### Docker Compose

Docker Compose manages the FastAPI and PostgreSQL containers.

This provides:

- Reproducible deployment
- Internal service networking
- Persistent database storage
- Simple service startup and restart
- Consistent local and server environments

### GitHub Actions

GitHub Actions provides automated CI/CD.

The current pipeline performs:

1. Checkout repository.
2. Set up Python 3.12.
3. Install dependencies.
4. Run automated tests.
5. Build the Docker image.
6. SSH into EC2.
7. Pull the latest `Main` branch.
8. Rebuild and restart the Docker Compose services.

## Security Boundaries

The public-facing boundary is Nginx.

External clients communicate with Nginx over HTTPS.

FastAPI and PostgreSQL communicate internally through Docker networking.

PostgreSQL does not need to be exposed publicly.

API authentication is handled using an API key.

SSH access is used for server administration and CI/CD deployment.

## Design Decisions

The architecture intentionally uses a single EC2 instance because the current workload is small.

Using Kubernetes, multiple application servers, a load balancer, and several managed services would add operational complexity and cost without providing meaningful benefits for the current assessment workload.

The architecture can evolve later by separating the application tier from the database tier and introducing load balancing, horizontal scaling, and asynchronous IoT ingestion.
