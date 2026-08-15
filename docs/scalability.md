# Scalability

## Scenario

The system must be able to evolve if Nova IoT Systems grows to:

- 500 farms
- 50 rooms per farm
- IoT sensors in each room
- Sensors periodically sending environmental readings

This represents a much larger ingestion workload than the current single-EC2 deployment.

The current architecture should therefore be treated as the starting point rather than the final production architecture.

## 1. Horizontal Application Scaling

The FastAPI application should remain stateless so multiple application instances can run simultaneously.

Instead of:

```text
Internet
   |
   v
Single EC2
   |
   v
FastAPI
```

the architecture could become:

```text
Internet
   |
   v
Load Balancer
   |
   +---- FastAPI Instance 1
   +---- FastAPI Instance 2
   +---- FastAPI Instance 3
```

Additional instances can be added when traffic increases.

## 2. Load Balancing

An AWS Application Load Balancer could distribute HTTP/HTTPS requests across multiple FastAPI instances.

The load balancer would also perform health checks and stop sending traffic to unhealthy instances.

This removes the single-application-instance bottleneck.

## 3. IoT Ingestion and MQTT

For large numbers of IoT devices, directly sending every sensor reading through a normal REST API may become inefficient.

MQTT would be a better protocol for device-to-cloud communication because it is lightweight and designed for IoT devices.

A possible architecture would be:

```text
IoT Sensors
    |
    | MQTT
    v
MQTT Broker
    |
    v
Message Queue / Stream
    |
    v
Processing Workers
    |
    v
Database
```

This separates device ingestion from normal API request handling.

## 4. Message Queues

A message queue would absorb sudden bursts of sensor traffic.

If many devices send readings at the same time, the queue can temporarily buffer messages instead of forcing the API and database to process everything immediately.

Workers can consume messages at a controlled rate.

Benefits include:

- Buffering
- Retry capability
- Fault tolerance
- Decoupling ingestion from processing

## 5. Database Scaling

PostgreSQL would eventually become a bottleneck if the number of readings grows significantly.

The database could be moved to a managed service such as Amazon RDS.

Possible improvements include:

- Larger database instances
- Read replicas
- Connection pooling
- Index optimization
- Partitioning time-series data
- Automated backups
- Database monitoring

Historical IoT readings could also be moved to cheaper object storage depending on retention requirements.

## 6. Caching

Frequently requested data can be cached.

For example, device metadata may not need to be fetched from PostgreSQL on every request.

A caching layer such as Redis could store frequently accessed data.

This reduces database load and improves response latency.

## 7. Container Orchestration

Docker Compose is sufficient for the current deployment but is not ideal for hundreds of application instances.

At larger scale, container orchestration such as Kubernetes or Amazon ECS could be introduced.

The orchestrator would handle:

- Container scheduling
- Service discovery
- Health checks
- Automatic restarts
- Horizontal scaling
- Rolling deployments

Kubernetes would not be introduced at the current scale because it would add significant operational complexity.

## 8. Monitoring at Scale

At larger scale, monitoring would cover:

- Per-service CPU and memory
- Request rate
- Request latency
- Error rate
- Queue depth
- MQTT connection count
- Database CPU
- Database connections
- Database storage
- Container health
- Sensor ingestion rate

Dashboards and alerts would be created around these metrics.

## 9. Cost Optimization

The architecture should scale based on actual workload rather than permanently running maximum capacity.

Cost optimization techniques include:

- Autoscaling application instances.
- Right-sizing compute instances.
- Using managed services where operational savings justify their cost.
- Storing older sensor data in cheaper storage.
- Setting log retention periods.
- Avoiding unnecessary always-on services.
- Batching sensor writes where appropriate.

## Target Architecture

A future production architecture could look like:

```text
IoT Sensors
     |
     | MQTT
     v
MQTT Broker
     |
     v
Message Queue
     |
     v
Processing Workers
     |
     +------------------+
     |                  |
     v                  v
 PostgreSQL/RDS       Object Storage
     |
     v
Redis Cache

Web/API Clients
     |
     v
Application Load Balancer
     |
     +---- FastAPI 1
     +---- FastAPI 2
     +---- FastAPI N
```

The key principle is to scale each part independently instead of simply making one EC2 instance larger.
