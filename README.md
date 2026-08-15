# Nova IoT Backend API

This is the minimal FastAPI backend for the Nova IoT Internship Assessment.

## Authentication

This API is protected via API keys as per the requirements.

### Configuration
You must configure the API key on the server by setting the `API_KEY` environment variable prior to booting the application (e.g. using `export API_KEY=my-secret-key` or via Docker Compose environment blocks). 
The `API_KEY` is also mocked out as an example inside `.env.example`.

### Making Requests
All endpoints (except the public `GET /health` endpoint) are secured. Clients must authenticate by sending the configured key inside the **`X-API-Key` HTTP Header**.

If the header is missing or incorrect, the server will return an `HTTP 401 Unauthorized`.

### Example Authenticated Request
Below is an example of pushing a sensor reading using `curl`:

```bash
curl -X POST http://127.0.0.1:8000/api/readings \
     -H "Content-Type: application/json" \
     -H "X-API-Key: your_api_key_here" \
     -d '{
           "device_id": "MUSHROOM-ROOM-001",
           "temperature": 23.8,
           "humidity": 87.4,
           "co2": 1180,
           "timestamp": "2026-08-10T10:30:00Z"
         }'
```
