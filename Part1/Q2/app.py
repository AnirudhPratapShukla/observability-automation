#!/usr/bin/env python3
"""REST API for rbcapp1 service status stored in Elasticsearch with OpenTelemetry."""

import os
from pathlib import Path

from elasticsearch import Elasticsearch, exceptions as es_exceptions
from flask import Flask, jsonify, request

from opentelemetry import metrics, trace
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


# -------------------------------------------------------------------
# Flask application
# -------------------------------------------------------------------

app = Flask(__name__)

ES_HOST = os.getenv("ES_HOST", "http://localhost:9200")
ES_USER = os.getenv("ES_USER")
ES_PASSWORD = os.getenv("ES_PASSWORD")
ES_INDEX = os.getenv("ES_INDEX", "service-status")

OTEL_ENDPOINT = os.getenv(
    "OTEL_EXPORTER_OTLP_ENDPOINT",
    "http://localhost:4317"
)


# -------------------------------------------------------------------
# OpenTelemetry setup
# -------------------------------------------------------------------

resource = Resource.create(
    {
        "service.name": "rbcapp1-status-api",
        "service.namespace": "rbcapp1",
        "deployment.environment": os.getenv(
            "ENVIRONMENT",
            "dev"
        ),
    }
)


# Tracing
tracer_provider = TracerProvider(resource=resource)

tracer_provider.add_span_processor(
    BatchSpanProcessor(
        OTLPSpanExporter(
            endpoint=OTEL_ENDPOINT,
            insecure=True,
        )
    )
)

trace.set_tracer_provider(tracer_provider)

tracer = trace.get_tracer("rbcapp1-status-api")


# Metrics
metric_exporter = OTLPMetricExporter(
    endpoint=OTEL_ENDPOINT,
    insecure=True,
)

metric_reader = PeriodicExportingMetricReader(
    metric_exporter,
    export_interval_millis=10000,
)

meter_provider = MeterProvider(
    resource=resource,
    metric_readers=[metric_reader],
)

metrics.set_meter_provider(meter_provider)

meter = metrics.get_meter("rbcapp1-status-api")

service_status_metric = meter.create_counter(
    "rbcapp1.service.status",
    description="UP/DOWN service status observations",
    unit="1",
)


# Automatically create Flask request spans
FlaskInstrumentor().instrument_app(app)


# -------------------------------------------------------------------
# Elasticsearch client
# -------------------------------------------------------------------

def create_es_client() -> Elasticsearch:
    """Create an Elasticsearch client from environment variables."""

    kwargs = {
        "hosts": [ES_HOST],
        "request_timeout": 10,
    }

    if ES_USER and ES_PASSWORD:
        kwargs["basic_auth"] = (ES_USER, ES_PASSWORD)

    return Elasticsearch(**kwargs)


es = create_es_client()


# -------------------------------------------------------------------
# Helper functions
# -------------------------------------------------------------------

def read_json_payload():
    """Read the JSON object sent to /add, including JSON-file uploads."""

    if request.is_json:
        return request.get_json(silent=True)

    uploaded = request.files.get("file")

    if uploaded:
        import json
        return json.load(uploaded.stream)

    return None


def record_service_status(service_name, service_status, host_name=None):
    """Record the current service status as an OpenTelemetry metric."""

    attributes = {
        "service_name": service_name,
        "service_status": service_status,
    }

    if host_name:
        attributes["host_name"] = host_name

    service_status_metric.add(
        1,
        attributes=attributes,
    )


# -------------------------------------------------------------------
# REST endpoints
# -------------------------------------------------------------------

@app.post("/add")
def add_status():

    with tracer.start_as_current_span("rbcapp1.add") as span:

        payload = read_json_payload()

        if not isinstance(payload, dict):
            span.set_attribute("service_status", "INVALID")

            return jsonify(
                {
                    "error": "A JSON object or JSON file is required"
                }
            ), 400

        required = {
            "service_name",
            "service_status",
            "host_name",
        }

        missing = sorted(
            required - payload.keys()
        )

        if missing:
            span.set_attribute(
                "service_status",
                "INVALID",
            )

            return jsonify(
                {
                    "error": "Missing required fields",
                    "fields": missing,
                }
            ), 400

        service_name = payload["service_name"]
        service_status = payload["service_status"]
        host_name = payload["host_name"]

        # Required span attributes
        span.set_attribute(
            "service_name",
            service_name,
        )

        span.set_attribute(
            "host_name",
            host_name,
        )

        span.set_attribute(
            "service_status",
            service_status,
        )

        # Record custom metric
        record_service_status(
            service_name,
            service_status,
            host_name,
        )

        try:

            # Child span covering Elasticsearch write
            with tracer.start_as_current_span(
                "elasticsearch.index"
            ) as es_span:

                es_span.set_attribute(
                    "elasticsearch.index",
                    ES_INDEX,
                )

                result = es.index(
                    index=ES_INDEX,
                    document=payload,
                )

            return jsonify(
                {
                    "message": "Indexed",
                    "id": result["_id"],
                    "index": result["_index"],
                }
            ), 201

        except (
            es_exceptions.ConnectionError,
            es_exceptions.ConnectionTimeout,
        ) as exc:

            span.record_exception(exc)
            span.set_attribute(
                "service_status",
                "DOWN",
            )

            app.logger.exception(
                "Elasticsearch connection failed"
            )

            return jsonify(
                {
                    "error": "Elasticsearch unavailable",
                    "details": str(exc),
                }
            ), 503

        except es_exceptions.ElasticsearchException as exc:

            span.record_exception(exc)

            app.logger.exception(
                "Elasticsearch request failed"
            )

            return jsonify(
                {
                    "error": "Elasticsearch error",
                    "details": str(exc),
                }
            ), 502


def latest_service_status(service_name: str):

    with tracer.start_as_current_span(
        "elasticsearch.search"
    ) as span:

        span.set_attribute(
            "service_name",
            service_name,
        )

        span.set_attribute(
            "elasticsearch.index",
            ES_INDEX,
        )

        response = es.search(
            index=ES_INDEX,
            query={
                "term": {
                    "service_name.keyword": service_name
                }
            },
            sort=[
                {
                    "@timestamp": {
                        "order": "desc"
                    }
                }
            ],
            size=1,
        )

        hits = response["hits"]["hits"]

        return (
            hits[0]["_source"]
            if hits
            else None
        )


@app.get("/healthcheck/<service_name>")
def service_healthcheck(service_name: str):

    with tracer.start_as_current_span(
        "rbcapp1.service_healthcheck"
    ) as span:

        span.set_attribute(
            "service_name",
            service_name,
        )

        try:

            status = latest_service_status(
                service_name
            )

        except (
            es_exceptions.ConnectionError,
            es_exceptions.ConnectionTimeout,
        ) as exc:

            span.record_exception(exc)

            span.set_attribute(
                "service_status",
                "DOWN",
            )

            return jsonify(
                {
                    "error": "Elasticsearch unavailable",
                    "details": str(exc),
                }
            ), 503

        except es_exceptions.ElasticsearchException as exc:

            span.record_exception(exc)

            span.set_attribute(
                "service_status",
                "DOWN",
            )

            return jsonify(
                {
                    "error": "Elasticsearch error",
                    "details": str(exc),
                }
            ), 502

        if status is None:

            span.set_attribute(
                "service_status",
                "UNKNOWN",
            )

            record_service_status(
                service_name,
                "UNKNOWN",
            )

            return jsonify(
                {
                    "service_name": service_name,
                    "service_status": "UNKNOWN",
                }
            ), 404

        service_status = status.get(
            "service_status",
            "UNKNOWN",
        )

        host_name = status.get(
            "host_name"
        )

        span.set_attribute(
            "service_status",
            service_status,
        )

        if host_name:
            span.set_attribute(
                "host_name",
                host_name,
            )

        record_service_status(
            service_name,
            service_status,
            host_name,
        )

        return jsonify(status), 200


@app.get("/healthcheck")
def application_healthcheck():

    with tracer.start_as_current_span(
        "rbcapp1.application_healthcheck"
    ) as span:

        try:

            with tracer.start_as_current_span(
                "elasticsearch.health_search"
            ) as es_span:

                es_span.set_attribute(
                    "elasticsearch.index",
                    ES_INDEX,
                )

                response = es.search(
                    index=ES_INDEX,
                    query={
                        "match_all": {}
                    },
                    sort=[
                        {
                            "@timestamp": {
                                "order": "desc"
                            }
                        }
                    ],
                    size=1000,
                )

            latest = {}

            for hit in response["hits"]["hits"]:

                source = hit["_source"]

                service = source.get(
                    "service_name"
                )

                if service and service not in latest:
                    latest[service] = source

            expected = {
                "httpd",
                "rabbitMQ",
                "postgreSQL",
            }

            statuses = {
                name: latest.get(
                    name,
                    {}
                ).get(
                    "service_status",
                    "UNKNOWN",
                )
                for name in expected
            }

            # Record UP/DOWN/UNKNOWN metrics
            for service_name, service_status in statuses.items():

                host_name = latest.get(
                    service_name,
                    {}
                ).get(
                    "host_name"
                )

                record_service_status(
                    service_name,
                    service_status,
                    host_name,
                )

            overall = (
                "UP"
                if statuses
                and all(
                    value == "UP"
                    for value in statuses.values()
                )
                else "DOWN"
            )

            span.set_attribute(
                "service_name",
                "rbcapp1",
            )

            span.set_attribute(
                "service_status",
                overall,
            )

            return jsonify(
                {
                    "application": "rbcapp1",
                    "application_status": overall,
                    "services": statuses,
                }
            ), 200

        except es_exceptions.NotFoundError:

            span.set_attribute(
                "service_status",
                "DOWN",
            )

            return jsonify(
                {
                    "application": "rbcapp1",
                    "application_status": "DOWN",
                    "error": "Index not found",
                }
            ), 503

        except (
            es_exceptions.ConnectionError,
            es_exceptions.ConnectionTimeout,
        ) as exc:

            span.record_exception(exc)

            span.set_attribute(
                "service_status",
                "DOWN",
            )

            return jsonify(
                {
                    "error": "Elasticsearch unavailable",
                    "details": str(exc),
                }
            ), 503

        except es_exceptions.ElasticsearchException as exc:

            span.record_exception(exc)

            span.set_attribute(
                "service_status",
                "DOWN",
            )

            return jsonify(
                {
                    "error": "Elasticsearch error",
                    "details": str(exc),
                }
            ), 502


@app.get("/")
def root():

    return jsonify(
        {
            "service": "rbcapp1-status-api",
            "endpoints": [
                "POST /add",
                "GET /healthcheck",
                "GET /healthcheck/<service_name>",
            ],
        }
    )


# -------------------------------------------------------------------
# Application startup
# -------------------------------------------------------------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(
            os.getenv(
                "PORT",
                "5000"
            )
        ),
        debug=False,
    )
