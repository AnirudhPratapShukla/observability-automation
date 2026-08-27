# Part 1 - Question 2

## REST service with Elasticsearch

The Flask application exposes:

- `POST /add` - accepts a JSON object or uploaded JSON file and indexes it into Elasticsearch.
- `GET /healthcheck` - calculates the overall `rbcapp1` status from the latest service status documents.
- `GET /healthcheck/<service_name>` - returns the latest status for one service.

## Environment variables

```bash
export ES_HOST=http://localhost:9200
export ES_USER=elastic
export ES_PASSWORD='your-password'
export ES_INDEX=service-status
```

Credentials are optional when Elasticsearch is running without authentication locally.

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

The API listens on port 5000 by default.

## Test

```bash
curl http://localhost:5000/healthcheck

curl http://localhost:5000/healthcheck/httpd

curl -X POST http://localhost:5000/add \
  -H 'Content-Type: application/json' \
  -d '{"service_name":"httpd","service_status":"UP","host_name":"host1","@timestamp":"2026-08-25T10:00:00Z"}'
```
