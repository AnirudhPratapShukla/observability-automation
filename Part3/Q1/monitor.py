#!/usr/bin/env python3
"""Monitor rbcapp1 services and write one JSON status file per service."""

import json
import os
import socket
import subprocess
from datetime import datetime, timezone
from pathlib import Path

SERVICES = {
    "httpd": "httpd",
    "rabbitMQ": "rabbitmq-server",
    "postgreSQL": "postgresql",
}

OUTPUT_DIR = Path(os.getenv("RBCAPP1_STATUS_DIR", "./output"))


def get_service_status(service_unit: str) -> str:
    """Return UP when systemd reports the service as active; otherwise DOWN."""
    result = subprocess.run(
        ["systemctl", "is-active", service_unit],
        capture_output=True,
        text=True,
        check=False,
    )
    return "UP" if result.returncode == 0 and result.stdout.strip() == "active" else "DOWN"


def timestamp_for_filename(timestamp: datetime) -> str:
    """Return a filesystem-safe UTC timestamp."""
    return timestamp.strftime("%Y%m%dT%H%M%SZ")


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    host_name = socket.gethostname()
    timestamp = datetime.now(timezone.utc)

    for service_name, service_unit in SERVICES.items():
        status = get_service_status(service_unit)
        payload = {
            "service_name": service_name,
            "service_status": status,
            "host_name": host_name,
            "@timestamp": timestamp.isoformat().replace("+00:00", "Z"),
        }

        filename = f"{service_name}-status-{timestamp_for_filename(timestamp)}.json"
        output_file = OUTPUT_DIR / filename
        output_file.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"{service_name}: {status} -> {output_file}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
