# Monitoring and Logging

## Monitoring Approach

The application uses application health checks, Nginx logs, Docker/container status, and AWS CloudWatch monitoring.

The assessment requires monitoring for application logs, CPU, memory, errors, API availability, and database health.

## Health Check

The application provides:

```text
GET /health
```

The endpoint returns:

```json
{
  "status": "ok",
  "message": "API is running"
}
```

This provides a simple way to verify that the API process is responding.

## Nginx Logs

Nginx produces:

```text
/var/log/nginx/access.log
/var/log/nginx/error.log
```

The CloudWatch Agent is configured to collect these logs.

This allows HTTP traffic and reverse-proxy errors to be investigated centrally.

## CloudWatch

CloudWatch is used for centralized monitoring and log collection.

Important metrics include:

### CPU Utilization

High CPU usage can indicate:

- Increased API traffic
- Expensive application operations
- Database-heavy operations
- Insufficient compute capacity

### Memory Utilization

Increasing memory usage can indicate:

- Memory leaks
- Too many application processes
- Container resource pressure
- Insufficient instance capacity

### Disk Usage

Disk usage should be monitored because PostgreSQL data, Docker images, container logs, and system logs consume storage.

### Network Traffic

Network metrics can help identify unexpected traffic increases or unusual application behavior.

### Application Availability

The `/health` endpoint provides a basic application availability check.

A production setup could periodically call this endpoint from an external monitoring system and alert when it fails.

### Database Health

PostgreSQL container health is monitored through Docker health checks.

Database monitoring should also track:

- Connection failures
- Query latency
- Connection count
- Disk usage
- Database availability

## Logs

The main log sources are:

```text
FastAPI application
Nginx access logs
Nginx error logs
Docker/container logs
PostgreSQL logs
```

These logs are useful for diagnosing application failures, HTTP errors, database issues, and deployment problems.

## Alerts

Useful production alerts would include:

- High CPU utilization
- High memory utilization
- Low disk space
- API health check failures
- Repeated HTTP 5xx responses
- PostgreSQL health failures
- Container restart loops

## What I Would Monitor in Production

The most important production signals would be:

1. **API availability** - Detect outages quickly.
2. **HTTP 5xx rate** - Detect application failures.
3. **Request latency** - Detect performance degradation.
4. **CPU and memory** - Identify resource saturation.
5. **Database health** - Detect database failures or bottlenecks.
6. **Disk usage** - Prevent storage exhaustion.
7. **Network traffic** - Detect abnormal traffic patterns.
8. **Container restarts** - Detect unstable services.

Monitoring should focus on both infrastructure health and user-facing application health.
