# Failure Scenario: API Unavailable

## Scenario

The public API suddenly becomes unavailable.

The investigation should proceed from the outside of the system toward the internal components.

```text
Client
  |
  v
DNS
  |
  v
Nginx / EC2
  |
  v
FastAPI
  |
  v
PostgreSQL
```

## Step 1: Confirm the Failure

First, verify that the issue is reproducible.

```bash
curl -I https://nova-iot-assessment-api.vedang.tech/health
```

Also test the health endpoint from another network if possible.

If the endpoint works locally but not externally, the problem is likely in networking, Nginx, HTTPS, or DNS.

## Step 2: Check DNS

Verify that the domain resolves to the expected public endpoint.

If DNS resolution fails, inspect the DNS record configuration.

If DNS resolves correctly, continue to the server.

## Step 3: Check EC2

Check whether the EC2 instance is running in AWS.

Then verify:

- Instance status
- System status checks
- CPU utilization
- Memory usage
- Disk usage
- Network activity

A resource exhaustion problem could prevent services from responding correctly.

## Step 4: Check Security Group

Verify that the required public ports are allowed.

Expected public ports include:

```text
22   SSH
80   HTTP
443  HTTPS
```

The database port should not be publicly exposed.

## Step 5: Check Nginx

On the EC2 instance:

```bash
sudo systemctl status nginx
```

If Nginx is stopped:

```bash
sudo systemctl restart nginx
```

Check Nginx configuration:

```bash
sudo nginx -t
```

Inspect logs:

```bash
sudo tail -50 /var/log/nginx/error.log
sudo tail -50 /var/log/nginx/access.log
```

## Step 6: Check Docker Containers

Run:

```bash
docker ps
```

Then:

```bash
docker compose -f docker/docker-compose.yml ps
```

If the FastAPI container is stopped, inspect its logs:

```bash
docker logs <api-container>
```

## Step 7: Check FastAPI Directly

Test the application from inside the server:

```bash
curl http://localhost:8000/health
```

If this succeeds but the public endpoint fails, FastAPI is probably healthy and the problem is likely Nginx, HTTPS, or networking.

If this fails, continue investigating the application container.

## Step 8: Check PostgreSQL

Check the PostgreSQL container:

```bash
docker ps
```

Inspect its logs:

```bash
docker logs <postgres-container>
```

Possible problems include:

- Database startup failure
- Connection exhaustion
- Invalid credentials
- Disk exhaustion
- Database errors

## Step 9: Check Application Logs

Inspect FastAPI logs:

```bash
docker logs <api-container>
```

Look for:

- Python exceptions
- Database connection errors
- Authentication errors
- Dependency failures
- Container restart loops

## Step 10: Check CloudWatch

CloudWatch should be checked for:

- CPU spikes
- Memory pressure
- Disk usage
- Nginx errors
- Repeated HTTP errors
- Application/container failures

This helps determine whether the outage is caused by infrastructure or the application.

## Step 11: Check Recent Deployment

Because the system uses CI/CD, check GitHub Actions for the most recent deployment.

If the outage started immediately after a deployment:

1. Check deployment logs.
2. Check application container logs.
3. Compare the deployed commit with the previous working commit.
4. Roll back to the previous known-good version if necessary.

## Troubleshooting Order

The investigation order is:

```text
1. Reproduce the issue
2. DNS
3. EC2 health
4. Security group/networking
5. Nginx
6. Docker containers
7. FastAPI
8. PostgreSQL
9. CloudWatch logs/metrics
10. Recent deployment
```

This approach starts at the user-facing layer and progressively moves inward, reducing unnecessary changes and helping isolate the failing component.
