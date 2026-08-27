#!/usr/bin/env python3
"""REST API for rbcapp1 service status stored in Elasticsearch."""

import os
from pathlib import Path

from elasticsearch import Elasticsearch, exceptions as es_exceptions
from flask import Flask, jsonify, request

app = Flask(__name__)

ES_HOST = os.getenv("ES_HOST", "http://localhost:9200")
ES_USER = os.getenv("ES_USER")
ES_PASSWORD = os.getenv("ES_PASSWORD")
ES_INDEX = os.getenv("ES_INDEX", "service-status")


def create_es_client() -> Elasticsearch:
    """Create an Elasticsearch client from environment variables."""
    kwargs = {"hosts": [ES_HOST], "request_timeout": 10}
    if ES_USER and ES_PASSWORD:
        kwargs["basic_auth"] = (ES_USER, ES_PASSWORD)
    return Elasticsearch(**kwargs)


es = create_es_client()


def read_json_payload():
    """Read the JSON object sent to /add, including JSON-file uploads."""
    if request.is_json:
        return request.get_json(silent=True)

    uploaded = request.files.get("file")
    if uploaded:
        import json
        return json.load(uploaded.stream)

    return None


@app.post("/add")
def add_status():
    payload = read_json_payload()
    if not isinstance(payload, dict):
        return jsonify({"error": "A JSON object or JSON file is required"}), 400

    required = {"service_name", "service_status", "host_name"}
    missing = sorted(required - payload.keys())
    if missing:
        return jsonify({"error": "Missing required fields", "fields": missing}), 400

    try:
        result = es.index(index=ES_INDEX, document=payload)
        return jsonify({"message": "Indexed", "id": result["_id"], "index": result["_index"]}), 201
    except (es_exceptions.ConnectionError, es_exceptions.ConnectionTimeout) as exc:
        app.logger.exception("Elasticsearch connection failed")
        return jsonify({"error": "Elasticsearch unavailable", "details": str(exc)}), 503
    except es_exceptions.ElasticsearchException as exc:
        app.logger.exception("Elasticsearch request failed")
        return jsonify({"error": "Elasticsearch error", "details": str(exc)}), 502


def latest_service_status(service_name: str):
    """Return the latest indexed status for one service."""
    response = es.search(
        index=ES_INDEX,
        query={"term": {"service_name.keyword": service_name}},
        sort=[{"@timestamp": {"order": "desc"}}],
        size=1,
    )
    hits = response["hits"]["hits"]
    return hits[0]["_source"] if hits else None


@app.get("/healthcheck/<service_name>")
def service_healthcheck(service_name: str):
    try:
        status = latest_service_status(service_name)
    except (es_exceptions.ConnectionError, es_exceptions.ConnectionTimeout) as exc:
        return jsonify({"error": "Elasticsearch unavailable", "details": str(exc)}), 503
    except es_exceptions.ElasticsearchException as exc:
        return jsonify({"error": "Elasticsearch error", "details": str(exc)}), 502

    if status is None:
        return jsonify({"service_name": service_name, "service_status": "UNKNOWN"}), 404

    return jsonify(status), 200


@app.get("/healthcheck")
def application_healthcheck():
    try:
        response = es.search(
            index=ES_INDEX,
            query={"match_all": {}},
            sort=[{"@timestamp": {"order": "desc"}}],
            size=1000
        )
        latest = {}
        for hit in response["hits"]["hits"]:
            source = hit["_source"]
            service = source.get("service_name")
            if service and service not in latest:
                latest[service] = source

        expected = {"httpd", "rabbitMQ", "postgreSQL"}
        statuses = {name: latest.get(name, {}).get("service_status", "UNKNOWN") for name in expected}
        overall = "UP" if statuses and all(value == "UP" for value in statuses.values()) else "DOWN"
        return jsonify({"application": "rbcapp1", "application_status": overall, "services": statuses}), 200
    except es_exceptions.NotFoundError:
        return jsonify({"application": "rbcapp1", "application_status": "DOWN", "error": "Index not found"}), 503
    except (es_exceptions.ConnectionError, es_exceptions.ConnectionTimeout) as exc:
        return jsonify({"error": "Elasticsearch unavailable", "details": str(exc)}), 503
    except es_exceptions.ElasticsearchException as exc:
        return jsonify({"error": "Elasticsearch error", "details": str(exc)}), 502


@app.get("/")
def root():
    return jsonify({"service": "rbcapp1-status-api", "endpoints": ["POST /add", "GET /healthcheck", "GET /healthcheck/<service_name>"]})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)
