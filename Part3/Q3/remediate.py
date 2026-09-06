#!/usr/bin/env python3

import os
import subprocess
from datetime import datetime, timezone

import requests
from elasticsearch import Elasticsearch


SERVICES = ["httpd", "rabbitMQ", "postgreSQL"]

REST_API_URL = os.getenv(
    "RBCAPP1_API_URL",
    "http://localhost:5000"
)

ES_HOST = os.getenv(
    "ES_HOST",
    "http://localhost:9200"
)

ES_USERNAME = os.getenv("ES_USERNAME")
ES_PASSWORD = os.getenv("ES_PASSWORD")

ES_INDEX = "service-remediation"


def check_service_status(service_name):
    """Check service status using the rbcapp1 REST API."""

    url = f"{REST_API_URL}/healthcheck/{service_name}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()

    except requests.RequestException as exc:
        print(f"Unable to check {service_name}: {exc}")
        return None


def restart_service(service_name):
    """Restart the Linux service using systemctl."""

    try:
        result = subprocess.run(
            ["sudo", "systemctl", "restart", service_name],
            capture_output=True,
            text=True,
            timeout=30
        )

        return result.returncode == 0, result.stderr.strip()

    except Exception as exc:
        return False, str(exc)


def create_elasticsearch_client():
    """Create Elasticsearch client using environment variables."""

    if ES_USERNAME and ES_PASSWORD:
        return Elasticsearch(
            ES_HOST,
            basic_auth=(ES_USERNAME, ES_PASSWORD)
        )

    return Elasticsearch(ES_HOST)


def log_result(es, service_name, initial_status, restart_success,
               final_status, message):

    document = {
        "@timestamp": datetime.now(timezone.utc).isoformat(),
        "service_name": service_name,
        "initial_status": initial_status,
        "restart_attempted": True,
        "restart_success": restart_success,
        "final_status": final_status,
        "message": message
    }

    try:
        es.index(
            index=ES_INDEX,
            document=document
        )

        print(f"Remediation result logged for {service_name}")

    except Exception as exc:
        print(f"Failed to log remediation result: {exc}")


def main():

    try:
        es = create_elasticsearch_client()
        es.info()
    except Exception as exc:
        print(f"Elasticsearch connection failed: {exc}")
        return 1

    for service in SERVICES:

        print(f"\nChecking service: {service}")

        initial_data = check_service_status(service)

        if not initial_data:
            continue

        initial_status = initial_data.get("service_status", "UNKNOWN")

        print(f"Initial status: {initial_status}")

        if initial_status != "DOWN":
            print(f"{service} is UP. No remediation required.")
            continue

        print(f"{service} is DOWN. Attempting restart...")

        restart_success, restart_message = restart_service(service)

        final_data = check_service_status(service)

        if final_data:
            final_status = final_data.get("service_status", "UNKNOWN")
        else:
            final_status = "UNKNOWN"

        print(f"Final status: {final_status}")

        if final_status == "UP":
            message = "Service restarted successfully and is UP."
        else:
            message = (
                "Service remains DOWN after restart attempt. "
                f"Restart message: {restart_message}"
            )

        log_result(
            es,
            service,
            initial_status,
            restart_success,
            final_status,
            message
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
