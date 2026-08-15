# Deployment

## Cloud Provider

- Provider: AWS
- Compute: Amazon EC2
- Operating system: Ubuntu
- Region: US East (N. Virginia)
- Container runtime: Docker
- Container management: Docker Compose
- Reverse proxy: Nginx

The public API is available through the configured HTTPS domain.

## Server Configuration

The EC2 instance hosts:

- Nginx
- FastAPI Docker container
- PostgreSQL Docker container
- CloudWatch Agent
- Docker Engine

The FastAPI application runs on port `8000`.

PostgreSQL runs on port `5432` inside the Docker environment.

Nginx handles public HTTP/HTTPS traffic.

## Initial Server Setup

The server was prepared by:

1. Creating an Ubuntu EC2 instance.
2. Configuring the EC2 security group.
3. Installing Docker.
4. Installing Docker Compose.
5. Cloning the GitHub repository.
6. Starting the application using Docker Compose.
7. Installing and configuring Nginx.
8. Configuring HTTPS using Let's Encrypt.
9. Installing and configuring the CloudWatch Agent.
10. Configuring GitHub Actions deployment.

## Docker Deployment

The application can be started with:

```bash
docker compose -f docker/docker-compose.yml up -d --build
```

Running containers can be checked using:

```bash
docker ps
```

The application health endpoint can be tested locally with:

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{
  "status": "ok",
  "message": "API is running"
}
```

## Nginx and HTTPS

Nginx acts as the public reverse proxy.

The request flow is:

```text
HTTPS Client
     |
     v
Nginx :443
     |
     v
FastAPI :8000
```

HTTPS is configured using a Let's Encrypt certificate.

## CI/CD Deployment

GitHub Actions is triggered when code is pushed to the `Main` branch.

The pipeline performs:

1. Checkout repository.
2. Set up Python 3.12.
3. Install dependencies.
4. Run automated tests.
5. Build the Docker image.
6. SSH into the EC2 instance.
7. Pull the latest `Main` branch.
8. Rebuild and restart Docker Compose services.

The deployment command is:

```bash
docker compose -f docker/docker-compose.yml up -d --build
```

The deployment credentials are stored as GitHub repository secrets rather than directly inside the workflow.

The EC2 deployment user is `ubuntu`.

## Environment Variables

Application configuration is supplied through environment variables.

Sensitive values such as:

- Database credentials
- API keys
- Application secrets

are not hardcoded into source code.

`.env` files containing secrets are excluded from Git.

## Verification

After deployment:

```bash
docker compose -f docker/docker-compose.yml ps
```

Then:

```bash
curl http://localhost:8000/health
```

The public HTTPS endpoint can then be tested from an external client.

## Deployment Trade-off

The current deployment uses a single EC2 instance because it is inexpensive and appropriate for the assessment.

The main limitation is that it is not highly available. A failure of the EC2 instance would make the application unavailable.

A production deployment at larger scale would use multiple application instances behind a load balancer.
